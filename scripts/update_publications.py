#!/usr/bin/env python3
"""Refresh _data/publications.yml from public scholarly indexes.

OpenAlex is queried by the ORCID in _config.yml. Semantic Scholar is then
searched for the same author, and an author record is kept only when one of
its papers shares a DOI already returned by OpenAlex. Papers already on the
site are kept. A listed preprint is replaced when a journal or conference
version of that same paper is found. Citation totals stay the OpenAlex
author counts.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "_config.yml"
DATA_PATH = ROOT / "_data" / "publications.yml"
USER_AGENT = "yaozhongjiang-homepage/1.0 (mailto:zhongjiang.yao@kcl.ac.uk)"

CONFERENCE_CODES = (
    ("association for computational linguistics", "ACL"),
    ("aaai conference on artificial intelligence", "AAAI"),
    ("acoustics, speech, and signal processing", "ICASSP"),
    ("international conference on acoustics", "ICASSP"),
    ("computer supported cooperative work in design", "CSCWD"),
    ("international joint conference on neural", "IJCNN"),
    ("european symposium on research in computer security", "ESORICS"),
    ("computer science and artificial intelligence", "CSAI"),
    ("parallel and distributed processing with applications", "IEEE ISPA"),
    ("international conference on communications", "ICC"),
    ("international conference on algorithms and architectures for parallel processing", "ICA3PP"),
    ("intelligent information processing", "IIP"),
    ("high performance computing and communications", "HPCC/SmartCity/DSS"),
    ("acm international conference on multimedia", "ACM MM"),
)

JOURNAL_NAMES = (
    ("journal of network and computer applications", "JNCA"),
    ("journal of parallel and distributed computing", "JPDC"),
    ("the computer journal", "The Computer Journal"),
    ("journal of software", "Journal of Software"),
    ("journal of cyber security", "Journal of Cyber Security"),
)


def orcid_from_config(text):
    match = re.search(r"orcid\s*:\s*['\"]?https?://orcid\.org/(\d{4}-\d{4}-\d{4}-\d{3}[\dX])", text)
    if not match:
        raise SystemExit("No ORCID URL found in _config.yml")
    return match.group(1)


def request_json(url, attempts=4):
    last_error = None
    for attempt in range(attempts):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=40) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code not in (429, 500, 502, 503, 504) or attempt == attempts - 1:
                raise
            time.sleep(2 ** attempt)
        except urllib.error.URLError as error:
            last_error = error
            if attempt == attempts - 1:
                raise
            time.sleep(2 ** attempt)
    raise last_error


def norm_title(title):
    text = (title or "").lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def doi_of(value):
    if not value:
        return ""
    match = re.search(r"(10\.\d{4,9}/[-._;()/:a-z0-9]+)", str(value), re.I)
    if not match:
        return ""
    return match.group(1).rstrip(".").lower()


def arxiv_of(value):
    if not value:
        return ""
    match = re.search(r"arxiv\.?org/(?:abs|pdf)/(\d{4}\.\d{4,5})", str(value), re.I)
    if match:
        return match.group(1)
    match = re.search(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})", str(value), re.I)
    return match.group(1) if match else ""


def kind_rank(kind):
    return {"preprint": 0, "conference": 2, "journal": 2}.get(kind, 1)


def venue_label(kind, year, venue, doi):
    blob = f"{venue or ''} {doi or ''}".lower()
    if kind == "preprint" or "arxiv" in blob:
        return "arXiv"
    for needle, code in CONFERENCE_CODES:
        if needle in blob:
            return f"{code} {year}" if year else code
    if doi.startswith("10.18653/"):
        return f"ACL {year}" if year else "ACL"
    if doi.startswith("10.1609/aaai"):
        return f"AAAI {year}" if year else "AAAI"
    for needle, name in JOURNAL_NAMES:
        if needle in blob:
            return name
    cleaned = re.sub(r"\s+", " ", venue or "").strip()
    return cleaned or "Publication"


def paper_url(doi, landing, arxiv):
    if arxiv:
        return f"https://arxiv.org/abs/{arxiv}"
    if doi:
        return f"https://doi.org/{doi}"
    return landing or ""


def person_key(name):
    return re.sub(r"[^a-z]", "", (name or "").lower())


def is_self(name):
    key = person_key(name)
    return "zhongjiang" in key and "yao" in key


def coauthor_keys(entries, source):
    keys = set()
    for entry in entries:
        if source == "openalex":
            name = ((entry.get("author") or {}).get("display_name")) or entry.get("raw_author_name")
        else:
            name = entry.get("name")
        if name and not is_self(name):
            keys.add(person_key(name))
    return keys


def skip_record(title, url):
    if not title or not title.strip():
        return True
    lowered = f"{title} {url}".lower()
    if "jglobal.jst.go.jp" in lowered or "powered by nict" in lowered:
        return True
    if re.search(r"[\u3040-\u30ff]", title):
        return True
    return False


def fetch_openalex(orcid):
    author = request_json(f"https://api.openalex.org/authors/https://orcid.org/{orcid}")
    author_id = author["id"].rsplit("/", 1)[-1]
    stats = author.get("summary_stats") or {}
    summary = {
        "citations": author.get("cited_by_count") or 0,
        "h_index": stats.get("h_index") or 0,
        "i10_index": stats.get("i10_index") or 0,
        "source": "OpenAlex",
    }
    cursor = "*"
    works = []
    while cursor:
        query = urllib.parse.urlencode({
            "filter": f"author.id:{author_id}",
            "per-page": 100,
            "cursor": cursor,
            "select": "display_name,publication_year,type,doi,cited_by_count,primary_location,authorships",
        })
        payload = request_json(f"https://api.openalex.org/works?{query}")
        for work in payload.get("results") or []:
            location = work.get("primary_location") or {}
            source = (location.get("source") or {}).get("display_name") or ""
            landing = location.get("landing_page_url") or ""
            doi = doi_of(work.get("doi") or "")
            arxiv = arxiv_of(doi) or arxiv_of(landing)
            preprint = bool(arxiv_of(doi) or work.get("type") == "preprint")
            if preprint:
                kind = "preprint"
                doi_out = ""
                arxiv_out = arxiv
                url = paper_url("", landing, arxiv_out)
            else:
                kind = classify_kind(work.get("type"), source, doi, "")
                doi_out = doi
                arxiv_out = arxiv_of(landing)
                url = paper_url(doi, landing, "")
            title = work.get("display_name") or ""
            if skip_record(title, landing):
                continue
            works.append({
                "title": title,
                "year": work.get("publication_year"),
                "kind": kind,
                "venue": venue_label(kind, work.get("publication_year"), source, doi_out),
                "url": url,
                "citations": work.get("cited_by_count"),
                "doi": doi_out,
                "arxiv": arxiv_out,
                "coauthors": coauthor_keys(work.get("authorships") or [], "openalex"),
                "origin": "openalex",
            })
        cursor = (payload.get("meta") or {}).get("next_cursor")
    return summary, works


def classify_kind(openalex_type, source, doi, arxiv):
    if arxiv or (source or "").lower().startswith("arxiv"):
        return "preprint"
    if openalex_type in ("article", "review", "journal-article"):
        return "journal"
    if openalex_type in ("proceedings-article", "conference-paper", "book-chapter"):
        return "conference"
    if doi.startswith("10.18653/") or doi.startswith("10.1609/aaai"):
        return "conference"
    return "conference" if source else "preprint"


def fetch_semantic_scholar(known_dois):
    if not known_dois:
        return []
    try:
        found = request_json(
            "https://api.semanticscholar.org/graph/v1/author/search?query="
            + urllib.parse.quote("Zhongjiang Yao")
            + "&limit=10"
        )
    except (urllib.error.URLError, urllib.error.HTTPError) as error:
        print(f"Semantic Scholar author search skipped: {error}", file=sys.stderr)
        return []
    accepted = []
    for author in found.get("data") or []:
        author_id = author.get("authorId")
        if not author_id:
            continue
        try:
            payload = request_json(
                "https://api.semanticscholar.org/graph/v1/author/"
                f"{author_id}/papers?limit=100&fields="
                + urllib.parse.quote(
                    "title,year,venue,url,citationCount,externalIds,authors,publicationTypes"
                )
            )
        except (urllib.error.URLError, urllib.error.HTTPError) as error:
            print(f"Semantic Scholar papers for {author_id} skipped: {error}", file=sys.stderr)
            continue
        papers = payload.get("data") or []
        dois = {doi_of((paper.get("externalIds") or {}).get("DOI")) for paper in papers}
        dois.discard("")
        if not (dois & known_dois):
            continue
        for paper in papers:
            names = " ".join((person.get("name") or "") for person in paper.get("authors") or [])
            if "zhongjiang" not in names.lower() or "yao" not in names.lower():
                continue
            external = paper.get("externalIds") or {}
            doi = doi_of(external.get("DOI"))
            arxiv = str(external.get("ArXiv") or "")
            if arxiv and not re.fullmatch(r"\d{4}\.\d{4,5}", arxiv):
                arxiv = arxiv_of(arxiv) or arxiv_of(doi)
            else:
                arxiv = arxiv or arxiv_of(doi) or arxiv_of(paper.get("url"))
            venue = paper.get("venue") or ""
            types = " ".join(paper.get("publicationTypes") or []).lower()
            preprint = (not doi) or doi.startswith("10.48550/arxiv")
            arxiv_out = arxiv or arxiv_of(doi)
            if preprint:
                kind = "preprint"
                doi_out = ""
                url = paper_url("", paper.get("url") or "", arxiv_out)
            elif "journal" in types:
                kind = "journal"
                doi_out = doi
                url = paper_url(doi, paper.get("url") or "", "")
            else:
                kind = "conference" if ("conference" in types or venue or doi) else "preprint"
                doi_out = "" if kind == "preprint" else doi
                url = paper_url(doi_out, paper.get("url") or "", arxiv_out if kind == "preprint" else "")
            title = paper.get("title") or ""
            if skip_record(title, url):
                continue
            accepted.append({
                "title": title,
                "year": paper.get("year"),
                "kind": kind,
                "venue": venue_label(kind, paper.get("year"), venue, doi_out),
                "url": url,
                "citations": paper.get("citationCount"),
                "doi": doi_out,
                "arxiv": arxiv_out,
                "coauthors": coauthor_keys(paper.get("authors") or [], "semantic-scholar"),
                "origin": "semantic-scholar",
            })
    return accepted


def identity_keys(record):
    keys = []
    if record.get("doi"):
        keys.append(("doi", record["doi"]))
    if record.get("arxiv"):
        keys.append(("arxiv", record["arxiv"]))
    return keys


def prefer_record(current, incoming):
    if current is None:
        return incoming
    if kind_rank(incoming["kind"]) > kind_rank(current["kind"]):
        chosen = dict(incoming)
        if current["origin"] == "openalex" and current.get("citations") is not None:
            chosen["citations"] = current["citations"]
            chosen["origin"] = "openalex"
        return chosen
    if kind_rank(incoming["kind"]) < kind_rank(current["kind"]):
        return current
    if incoming["origin"] == "openalex" and current["origin"] != "openalex":
        return incoming
    if current.get("citations") is None and incoming.get("citations") is not None:
        current = dict(current)
        current["citations"] = incoming["citations"]
    return current


def combine_records(records):
    records = [record for record in records if record.get("year")]
    parent = list(range(len(records)))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left, right):
        parent[find(left)] = find(right)

    seen = {}
    for index, record in enumerate(records):
        for key in identity_keys(record):
            if key in seen:
                union(index, seen[key])
            else:
                seen[key] = index
    groups = {}
    for index, record in enumerate(records):
        groups.setdefault(find(index), []).append(record)
    combined = []
    for group in groups.values():
        chosen = None
        arxiv = ""
        coauthors = set()
        for record in group:
            chosen = prefer_record(chosen, record)
            arxiv = arxiv or record.get("arxiv") or ""
            coauthors.update(record.get("coauthors") or ())
        if chosen is not None:
            chosen = dict(chosen)
            chosen["arxiv"] = chosen.get("arxiv") or arxiv
            chosen["coauthors"] = coauthors
            combined.append(chosen)
    return combined


def annotate(paper):
    annotated = dict(paper)
    annotated["_doi"] = doi_of(paper.get("url"))
    annotated["_arxiv"] = arxiv_of(paper.get("url"))
    return annotated


def title_matches(paper, record):
    left = norm_title(paper.get("title"))
    right = norm_title(record.get("title"))
    if not left or not right:
        return False
    if left == right:
        return True
    return SequenceMatcher(None, left, right).ratio() >= 0.92


def find_match(papers, record):
    if record.get("doi"):
        for paper in papers:
            if paper.get("_doi") == record["doi"]:
                return paper
    if record.get("arxiv"):
        for paper in papers:
            if paper.get("_arxiv") == record["arxiv"]:
                return paper
    matches = [paper for paper in papers if title_matches(paper, record)]
    if len(matches) == 1:
        return matches[0]
    return None


def apply_record(paper, record):
    changed = False
    if record.get("citations") is not None and paper.get("citations") != record["citations"]:
        if record["origin"] == "openalex" or "citations" not in paper:
            paper["citations"] = record["citations"]
            changed = True
    if kind_rank(record["kind"]) > kind_rank(paper.get("kind")):
        same_title = [item for item in (paper.get("_peers") or [paper]) if title_matches(item, record)]
        if len(same_title) == 1:
            for field in ("title", "venue", "year", "kind", "url"):
                if record.get(field) and paper.get(field) != record[field]:
                    paper[field] = record[field]
                    changed = True
            paper["_doi"] = record.get("doi") or ""
            paper["_arxiv"] = record.get("arxiv") or ""
    if not paper.get("url") and record.get("url"):
        paper["url"] = record["url"]
        paper["_doi"] = record.get("doi") or paper.get("_doi") or ""
        paper["_arxiv"] = record.get("arxiv") or paper.get("_arxiv") or ""
        changed = True
    return changed


def insert_new(papers, record):
    fresh = {
        "title": record["title"],
        "venue": record["venue"],
        "year": record["year"],
        "kind": record["kind"],
        "url": record.get("url") or "",
    }
    if record.get("citations") is not None:
        fresh["citations"] = record["citations"]
    for index, paper in enumerate(papers):
        if paper.get("year", 0) < record["year"]:
            papers.insert(index, annotate(fresh))
            return
        if paper.get("year") == record["year"]:
            papers.insert(index, annotate(fresh))
            return
    papers.append(annotate(fresh))


def yearly_rows(papers):
    if not papers:
        return []
    years = [paper["year"] for paper in papers if paper.get("year")]
    rows = []
    for year in range(min(years), max(years) + 1):
        selected = [paper for paper in papers if paper.get("year") == year]
        rows.append({
            "year": year,
            "papers": len(selected),
            "citations": sum(paper.get("citations") or 0 for paper in selected),
        })
    return rows


def merge_publications(existing, fetched, summary, updated):
    papers = [annotate(paper) for paper in existing.get("papers") or []]
    for paper in papers:
        paper["_peers"] = papers
    added = []
    updated_titles = []
    known_coauthors = set()
    for record in fetched:
        if record.get("origin") == "openalex":
            known_coauthors.update(record.get("coauthors") or ())
    for record in combine_records(fetched):
        match = find_match(papers, record)
        if match:
            if apply_record(match, record):
                updated_titles.append(match["title"])
            continue
        if any(title_matches(paper, record) for paper in papers):
            continue
        linked = record.get("origin") == "openalex" or bool(set(record.get("coauthors") or ()) & known_coauthors)
        if not linked:
            continue
        insert_new(papers, record)
        added.append(record["title"])
    cleaned = []
    for paper in papers:
        item = {
            "title": paper["title"],
            "venue": paper.get("venue") or "",
            "year": paper.get("year"),
            "kind": paper.get("kind") or "conference",
            "url": paper.get("url") or "",
        }
        if "citations" in paper and paper["citations"] is not None:
            item["citations"] = paper["citations"]
        if "recent" in paper:
            item["recent"] = paper["recent"]
        cleaned.append(item)
    stats = dict(summary)
    stats["updated"] = updated
    return {
        "stats": stats,
        "yearly": yearly_rows(cleaned),
        "papers": cleaned,
        "added": added,
        "updated_titles": updated_titles,
    }


def yaml_quote(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_yaml(data):
    lines = [
        "# Publication list refreshed by scripts/update_publications.py.",
        "# OpenAlex is queried with the ORCID in _config.yml. Semantic Scholar",
        "# records are added only when that author already shares an OpenAlex DOI.",
        "# Papers already listed here are kept. Citation totals are OpenAlex",
        "# author counts. A paper with no matched count omits citations.",
        "stats:",
        f"  citations: {int(data['stats']['citations'])}",
        f"  h_index: {int(data['stats']['h_index'])}",
        f"  i10_index: {int(data['stats']['i10_index'])}",
        f"  source: {yaml_quote(data['stats'].get('source') or 'OpenAlex')}",
        f"  updated: {yaml_quote(data['stats']['updated'])}",
        "yearly:",
    ]
    for row in data["yearly"]:
        lines.append(f"  - year: {int(row['year'])}")
        lines.append(f"    papers: {int(row['papers'])}")
        lines.append(f"    citations: {int(row['citations'])}")
    lines.append("papers:")
    for paper in data["papers"]:
        lines.append(f"  - title: {yaml_quote(paper['title'])}")
        lines.append(f"    venue: {yaml_quote(paper.get('venue') or '')}")
        lines.append(f"    year: {int(paper['year'])}")
        lines.append(f"    kind: {yaml_quote(paper.get('kind') or '')}")
        lines.append(f"    url: {yaml_quote(paper.get('url') or '')}")
        if "citations" in paper:
            lines.append(f"    citations: {int(paper['citations'])}")
        if "recent" in paper:
            lines.append(f"    recent: {'true' if paper['recent'] else 'false'}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def load_publications(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main():
    parser = argparse.ArgumentParser(description="Update publications from OpenAlex and Semantic Scholar.")
    parser.add_argument("--dry-run", action="store_true", help="Print the changes without writing the data file.")
    args = parser.parse_args()
    orcid = orcid_from_config(CONFIG_PATH.read_text(encoding="utf-8"))
    summary, openalex_works = fetch_openalex(orcid)
    known_dois = {record["doi"] for record in openalex_works if record.get("doi")}
    scholar_works = fetch_semantic_scholar(known_dois)
    existing = load_publications(DATA_PATH)
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    merged = merge_publications(existing, openalex_works + scholar_works, summary, updated)
    rendered = render_yaml(merged)
    print(f"OpenAlex works: {len(openalex_works)}")
    print(f"Semantic Scholar works from matched authors: {len(scholar_works)}")
    print(f"Added: {len(merged['added'])}")
    for title in merged["added"]:
        print(f"  + {title}")
    print(f"Updated: {len(merged['updated_titles'])}")
    for title in merged["updated_titles"]:
        print(f"  ~ {title}")
    if args.dry_run:
        return 0
    current = DATA_PATH.read_text(encoding="utf-8") if DATA_PATH.exists() else ""
    if current == rendered:
        print("No changes.")
        return 0
    DATA_PATH.write_text(rendered, encoding="utf-8")
    print(f"Wrote {DATA_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
