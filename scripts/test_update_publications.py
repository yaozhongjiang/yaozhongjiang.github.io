import unittest

from update_publications import merge_publications, norm_title, venue_label


SUMMARY = {"citations": 10, "h_index": 2, "i10_index": 1, "source": "OpenAlex"}


def record(**kwargs):
    base = {
        "title": "Example Paper",
        "year": 2026,
        "kind": "conference",
        "venue": "ACL 2026",
        "url": "https://doi.org/10.18653/v1/2026.acl-long.1",
        "citations": 3,
        "doi": "10.18653/v1/2026.acl-long.1",
        "arxiv": "",
        "origin": "openalex",
    }
    base.update(kwargs)
    return base


class MergeTests(unittest.TestCase):
    def test_keeps_unmatched_manual_paper(self):
        existing = {"papers": [{
            "title": "中文综述",
            "venue": "Journal of Software",
            "year": 2018,
            "kind": "journal",
            "url": "http://dx.doi.org/10.13328/j.cnki.jos.005620",
        }]}
        merged = merge_publications(existing, [], SUMMARY, "2026-10-01")
        self.assertEqual(merged["papers"][0]["title"], "中文综述")
        self.assertNotIn("citations", merged["papers"][0])

    def test_updates_citations_by_doi(self):
        existing = {"papers": [{
            "title": "EthGAN: Improving Ethereum Account Classification Accurary via Data Augmentation",
            "venue": "IJCNN 2024",
            "year": 2024,
            "kind": "conference",
            "url": "https://ieeexplore.ieee.org/document/10650065",
            "citations": 2,
        }]}
        fetched = [record(
            title="EthGAN: Improving Ethereum Account Classification Accuracy via Data Augmentation",
            year=2024,
            kind="conference",
            venue="IJCNN 2024",
            url="https://doi.org/10.1109/ijcnn60899.2024.10650065",
            citations=9,
            doi="",
            origin="openalex",
        )]
        merged = merge_publications(existing, fetched, SUMMARY, "2026-10-01")
        self.assertEqual(len(merged["papers"]), 1)
        self.assertEqual(merged["papers"][0]["citations"], 9)
        self.assertEqual(merged["papers"][0]["venue"], "IJCNN 2024")

    def test_does_not_collapse_journal_and_preprint(self):
        title = "Can LLMs Deeply Detect Complex Malicious Queries?"
        existing = {"papers": [
            {"title": title, "venue": "The Computer Journal", "year": 2024, "kind": "journal",
             "url": "https://doi.org/10.1093/comjnl/bxae124", "citations": 9},
            {"title": title, "venue": "arXiv", "year": 2024, "kind": "preprint",
             "url": "https://arxiv.org/abs/2405.03654", "citations": 1},
        ]}
        fetched = [
            record(title=title, year=2024, kind="journal", venue="The Computer Journal",
                   url="https://doi.org/10.1093/comjnl/bxae124", citations=11,
                   doi="10.1093/comjnl/bxae124", arxiv=""),
            record(title=title, year=2024, kind="preprint", venue="arXiv",
                   url="https://arxiv.org/abs/2405.03654", citations=2,
                   doi="", arxiv="2405.03654", origin="openalex"),
        ]
        merged = merge_publications(existing, fetched, SUMMARY, "2026-10-01")
        self.assertEqual(len(merged["papers"]), 2)
        self.assertEqual(merged["papers"][0]["citations"], 11)
        self.assertEqual(merged["papers"][1]["citations"], 2)
        self.assertEqual(merged["papers"][0]["venue"], "The Computer Journal")

    def test_upgrades_a_single_preprint(self):
        existing = {"papers": [{
            "title": "FAIRGAMER: Evaluating Social Biases in LLM-Based Video Game NPCs",
            "venue": "arXiv",
            "year": 2025,
            "kind": "preprint",
            "url": "https://arxiv.org/abs/2508.17825",
            "citations": 0,
        }]}
        fetched = [record(
            title="FAIRGAMER: Evaluating Social Biases in LLM-Based Video Game NPCs",
            year=2026,
            kind="conference",
            venue="ACL 2026",
            url="https://aclanthology.org/2026.acl-long.2015/",
            citations=0,
            doi="10.18653/v1/2026.acl-long.2015",
            arxiv="2508.17825",
            origin="semantic-scholar",
        )]
        merged = merge_publications(existing, fetched, SUMMARY, "2026-10-01")
        self.assertEqual(len(merged["papers"]), 1)
        self.assertEqual(merged["papers"][0]["venue"], "ACL 2026")
        self.assertEqual(merged["papers"][0]["year"], 2026)
        self.assertEqual(merged["papers"][0]["kind"], "conference")

    def test_adds_a_new_paper_ahead_of_older_years(self):
        existing = {"papers": [{
            "title": "Older",
            "venue": "ICC",
            "year": 2019,
            "kind": "conference",
            "url": "https://doi.org/10.1109/icc.2019.1",
            "citations": 1,
        }]}
        fetched = [record(title="Brand New Result", doi="10.1609/aaai.v40i18.1",
                          url="https://doi.org/10.1609/aaai.v40i18.1", venue="AAAI 2026")]
        merged = merge_publications(existing, fetched, SUMMARY, "2026-10-01")
        self.assertEqual([paper["title"] for paper in merged["papers"]], ["Brand New Result", "Older"])
        self.assertEqual(merged["added"], ["Brand New Result"])

    def test_yearly_fills_empty_years(self):
        existing = {"papers": [
            {"title": "A", "venue": "ICC", "year": 2018, "kind": "conference", "url": "https://doi.org/10.1/a", "citations": 4},
            {"title": "B", "venue": "ICC", "year": 2020, "kind": "conference", "url": "https://doi.org/10.1/b"},
        ]}
        merged = merge_publications(existing, [], SUMMARY, "2026-10-01")
        self.assertEqual(merged["yearly"], [
            {"year": 2018, "papers": 1, "citations": 4},
            {"year": 2019, "papers": 0, "citations": 0},
            {"year": 2020, "papers": 1, "citations": 0},
        ])

    def test_skips_unrelated_namesake(self):
        existing = {"papers": [{
            "title": "On the Prevention of Invalid Route Injection Attack",
            "venue": "IIP",
            "year": 2014,
            "kind": "conference",
            "url": "https://doi.org/10.1007/978-3-662-44980-6_33",
            "citations": 1,
        }]}
        fetched = [
            record(
                title="On the Prevention of Invalid Route Injection Attack",
                year=2014,
                venue="IIP",
                url="https://doi.org/10.1007/978-3-662-44980-6_33",
                doi="10.1007/978-3-662-44980-6_33",
                coauthors={"jingangliu"},
            ),
            record(
                title="Passive Location Accuracy of the Warning Aircraft",
                year=2010,
                venue="Publication",
                url="",
                doi="",
                arxiv="",
                citations=0,
                origin="semantic-scholar",
                coauthors=set(),
            ),
        ]
        merged = merge_publications(existing, fetched, SUMMARY, "2026-10-01")
        self.assertEqual([paper["title"] for paper in merged["papers"]], [
            "On the Prevention of Invalid Route Injection Attack",
        ])

    def test_venue_labels(self):
        self.assertEqual(venue_label("conference", 2026, "Proceedings of the AAAI Conference on Artificial Intelligence", ""), "AAAI 2026")
        self.assertEqual(norm_title("Hello, World!"), "hello world")


if __name__ == "__main__":
    unittest.main()
