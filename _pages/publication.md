---
permalink: /publication/
title: "Publications"
excerpt: ""
author_profile: false
---

{% assign journal_count = 0 %}
{% assign conference_count = 0 %}
{% assign preprint_count = 0 %}
{% for paper in site.data.publications.papers %}
  {% if paper.kind == "journal" %}
    {% assign journal_count = journal_count | plus: 1 %}
  {% elsif paper.kind == "conference" %}
    {% assign conference_count = conference_count | plus: 1 %}
  {% elsif paper.kind == "preprint" %}
    {% assign preprint_count = preprint_count | plus: 1 %}
  {% endif %}
{% endfor %}

<div class="site-wrap">
  <h1 class="page-heading">Publications</h1>

  <p class="profile-links">
    {% if site.author.dblp %}
      <a href="{{ site.author.dblp }}"><img class="brand-icon" src="{{ '/images/logos/dblp.png' | relative_url }}" alt="" width="48" height="18"> DBLP</a>
    {% endif %}
    {% if site.author.googlescholar %}
      <a href="{{ site.author.googlescholar }}"><img class="brand-icon brand-icon--scholar" src="{{ '/images/logos/scholar.svg' | relative_url }}" alt="" width="18" height="18"> Google Scholar</a>
    {% endif %}
    {% if site.author.linkedin %}
      {% include linkedin-url.html %}
      <a href="{{ linkedin_url }}" title="https://www.linkedin.com/in/zhongjiang-yao-b0756a406/"><img class="brand-icon" src="{{ '/images/logos/linkedin.svg' | relative_url }}" alt="" width="18" height="18"> LinkedIn</a>
    {% endif %}
    {% if site.author.orcid %}
      <a href="{{ site.author.orcid }}"><img class="brand-icon" src="{{ '/images/logos/orcid.svg' | relative_url }}" alt="" width="18" height="18"> ORCID</a>
    {% endif %}
  </p>

  <div class="two-col stat-grid">
    <section class="panel">
      <h2>Papers</h2>
      <div class="year-chart" data-key="papers" aria-label="Papers by year"></div>
      <p><strong>Journal papers</strong> {{ journal_count }}</p>
      <p><strong>Conference papers</strong> {{ conference_count }}</p>
      <p><strong>Preprints</strong> {{ preprint_count }}</p>
    </section>
    <section class="panel">
      <h2>Citations</h2>
      <div class="year-chart" data-key="citations" aria-label="Citations by year"></div>
      <p><strong>Citations</strong> {{ site.data.publications.stats.citations }}</p>
      <p><strong>h-index</strong> {{ site.data.publications.stats.h_index }}</p>
      <p><strong>i10-index</strong> {{ site.data.publications.stats.i10_index }}</p>
    </section>
  </div>
  <p class="stat-note">Lines show papers and citation counts by publication year. A year with no papers or citations is drawn as zero. The list is refreshed from OpenAlex and Semantic Scholar for ORCID 0000-0001-6583-9526{% if site.data.publications.stats.updated %} (last checked {{ site.data.publications.stats.updated }}){% endif %}. The citation total, h-index, and i10-index are the OpenAlex author counts.</p>
  <script id="yearly-data" type="application/json">{{ site.data.publications.yearly | jsonify }}</script>
  <script src="{{ '/assets/js/year-charts.js' | relative_url }}"></script>

  <div class="pub-table-wrap">
    <table class="pub-table">
      <thead>
        <tr>
          <th class="num">#</th>
          <th>Title</th>
          <th>Venue</th>
          <th class="num" aria-sort="none"><button type="button" class="pub-sort" data-sort="year" aria-pressed="false">Year</button></th>
          <th class="num" aria-sort="none"><button type="button" class="pub-sort" data-sort="citations" aria-pressed="false">Citation</button></th>
        </tr>
      </thead>
      <tbody>
        {% for paper in site.data.publications.papers %}
        <tr>
          <td class="num">{{ forloop.index }}</td>
          <td{% if paper.figure %} class="pub-title-cell"{% endif %}>
            {% if paper.url != "" %}
              <a href="{{ paper.url }}"{% if paper.figure %} class="pub-title" aria-expanded="false"{% endif %}>{{ paper.title }}</a>
            {% else %}
              {{ paper.title }}
            {% endif %}
            {% if paper.figure %}
            <div class="pub-expand">
              <div class="pub-expand-inner">
                <div class="pub-expand-body">
                  <img src="{{ paper.figure | relative_url }}" alt="{{ paper.figure_label | escape }}" width="{{ paper.figure_width }}" height="{{ paper.figure_height }}" decoding="async">
                  {% if paper.figure_label %}<p class="pub-expand-label">{{ paper.figure_label | escape }}</p>{% endif %}
                  {% if paper.task %}<p class="pub-task">{{ paper.task | escape }}</p>{% endif %}
                  {% if paper.claim %}<p class="pub-claim">{{ paper.claim | escape }}</p>{% endif %}
                </div>
              </div>
            </div>
            {% endif %}
          </td>
          <td>{{ paper.venue }}</td>
          <td class="num">{{ paper.year }}</td>
          <td class="num">{% if paper.citations != nil %}{{ paper.citations }}{% else %}—{% endif %}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
<script>
  (function () {
    var table = document.querySelector(".pub-table");
    if (!table || !table.tBodies[0]) return;
    var tbody = table.tBodies[0];
    var buttons = table.querySelectorAll("button.pub-sort");
    if (!buttons.length) return;
    var rows = [];
    for (var i = 0; i < tbody.rows.length; i++) rows.push(tbody.rows[i]);

    function numberIn(row, col) {
      var text = row.cells[col].textContent.replace(/^\s+|\s+$/g, "");
      if (!/^-?\d+$/.test(text)) return null;
      return parseInt(text, 10);
    }

    function sortBy(kind) {
      var col = kind === "year" ? 3 : 4;
      var ordered = [];
      for (var i = 0; i < rows.length; i++) ordered.push({ row: rows[i], i: i });
      ordered.sort(function (a, b) {
        var av = numberIn(a.row, col);
        var bv = numberIn(b.row, col);
        if (av === null && bv === null) return a.i - b.i;
        if (av === null) return 1;
        if (bv === null) return -1;
        if (bv !== av) return bv - av;
        return a.i - b.i;
      });
      for (var n = 0; n < ordered.length; n++) {
        ordered[n].row.cells[0].textContent = String(n + 1);
        tbody.appendChild(ordered[n].row);
      }
      for (var b = 0; b < buttons.length; b++) {
        var on = buttons[b].getAttribute("data-sort") === kind;
        if (on) buttons[b].classList.add("is-active");
        else buttons[b].classList.remove("is-active");
        buttons[b].setAttribute("aria-pressed", on ? "true" : "false");
        var th = buttons[b].parentNode;
        if (th && th.getAttribute) th.setAttribute("aria-sort", on ? "descending" : "none");
      }
    }

    for (var c = 0; c < buttons.length; c++) {
      buttons[c].addEventListener("click", function () {
        sortBy(this.getAttribute("data-sort"));
      });
    }
  })();
</script>
<script id="pub-expand-script">
  (function () {
    var cells = document.querySelectorAll(".pub-title-cell");
    if (!cells.length) return;
    var current = null;
    var keyboard = false;
    var keyboardOpen = false;
    var pinned = false;
    var hideTimer = null;

    function touchUi() {
      return window.matchMedia("(hover: none) and (pointer: coarse)").matches;
    }

    function isMouse(event) {
      return !event.pointerType || event.pointerType === "mouse";
    }

    function setExpanded(cell, open) {
      var link = cell.querySelector(".pub-title");
      if (link) link.setAttribute("aria-expanded", open ? "true" : "false");
    }

    function closeCell(cell) {
      if (!cell) return;
      cell.classList.remove("is-open");
      setExpanded(cell, false);
      if (current === cell) {
        current = null;
        pinned = false;
        keyboardOpen = false;
      }
    }

    function openCell(cell) {
      clearTimeout(hideTimer);
      if (current && current !== cell) closeCell(current);
      current = cell;
      cell.classList.add("is-open");
      setExpanded(cell, true);
    }

    function scheduleClose(cell) {
      clearTimeout(hideTimer);
      hideTimer = setTimeout(function () {
        if (pinned && touchUi()) return;
        if (cell.matches(":hover")) return;
        if (keyboardOpen && cell.contains(document.activeElement)) return;
        closeCell(cell);
      }, 40);
    }

    for (var i = 0; i < cells.length; i++) {
      (function (cell) {
        var link = cell.querySelector(".pub-title");
        cell.addEventListener("pointerenter", function (event) {
          if (!isMouse(event)) return;
          pinned = false;
          keyboardOpen = false;
          openCell(cell);
        });
        cell.addEventListener("pointerleave", function (event) {
          if (!isMouse(event)) return;
          scheduleClose(cell);
        });
        if (!link) return;
        link.addEventListener("focus", function () {
          if (!keyboard) return;
          keyboard = false;
          keyboardOpen = true;
          pinned = false;
          openCell(cell);
        });
        link.addEventListener("blur", function () {
          keyboardOpen = false;
          if (pinned) return;
          scheduleClose(cell);
        });
        link.addEventListener("click", function (event) {
          if (!touchUi()) return;
          if (cell.classList.contains("is-open") && pinned) return;
          event.preventDefault();
          pinned = true;
          keyboardOpen = false;
          openCell(cell);
        });
      })(cells[i]);
    }

    document.addEventListener("keydown", function (event) {
      if (event.key === "Tab") keyboard = true;
      if (event.key === "Escape") closeCell(current);
    });

    document.addEventListener("pointerdown", function (event) {
      if (!pinned || !current) return;
      if (current.contains(event.target)) return;
      closeCell(current);
    });

    window.addEventListener("scroll", function () {
      if (pinned) closeCell(current);
    }, true);
  })();
</script>
</div>
