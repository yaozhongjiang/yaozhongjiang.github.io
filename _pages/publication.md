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
          <td>
            {% if paper.url != "" %}
              <a href="{{ paper.url }}"{% if paper.figure %} class="pub-title" data-figure="{{ paper.figure | relative_url }}"{% if paper.figure_label %} data-figure-label="{{ paper.figure_label | escape }}"{% endif %}{% endif %}>{{ paper.title }}</a>
            {% else %}
              {{ paper.title }}
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
<div class="pub-hover" id="pub-hover" role="tooltip" aria-hidden="true">
  <img alt="" decoding="async">
  <p class="pub-hover-label" hidden></p>
</div>
<script>
  (function () {
    var popup = document.getElementById("pub-hover");
    var img = popup.querySelector("img");
    var label = popup.querySelector(".pub-hover-label");
    var triggers = document.querySelectorAll(".pub-title[data-figure]");
    if (!popup || !triggers.length) return;
    document.body.appendChild(popup);

    var current = null;
    var pinned = false;
    var keyboardOpen = false;
    var hideTimer = null;
    var shownAt = 0;
    var keyboard = false;

    function tapMode() {
      return window.matchMedia("(hover: none), (pointer: coarse), (max-width: 760px)").matches;
    }

    function overlaps(a, b) {
      return a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
    }

    function place(anchor) {
      var margin = 8;
      var gap = 8;
      var title = anchor.getBoundingClientRect();
      var width = popup.offsetWidth;
      var height = popup.offsetHeight;
      var left = title.left;
      if (left + width > window.innerWidth - margin) left = window.innerWidth - margin - width;
      if (left < margin) left = margin;
      var below = title.bottom + gap;
      var above = title.top - gap - height;
      var top = below;
      var placedAbove = false;
      if (below + height > window.innerHeight - margin && above >= margin) {
        top = above;
        placedAbove = true;
      }
      if (top < margin) top = margin;
      if (top + height > window.innerHeight - margin) top = Math.max(margin, window.innerHeight - margin - height);
      var box = { left: left, top: top, right: left + width, bottom: top + height };
      if (overlaps(box, title)) {
        if (title.top - margin > window.innerHeight - title.bottom) {
          top = Math.max(margin, title.top - gap - height);
          placedAbove = true;
        } else {
          top = Math.min(window.innerHeight - margin - height, title.bottom + gap);
          placedAbove = false;
        }
      }
      popup.style.left = Math.round(left) + "px";
      popup.style.top = Math.round(top) + "px";
      popup.style.transformOrigin = placedAbove ? "center bottom" : "center top";
      if (placedAbove) popup.classList.add("is-above");
      else popup.classList.remove("is-above");
    }

    function open(anchor) {
      shownAt = Date.now();
      place(anchor);
      popup.classList.add("is-open");
      popup.setAttribute("aria-hidden", "false");
      anchor.setAttribute("aria-describedby", "pub-hover");
    }

    function show(anchor) {
      clearTimeout(hideTimer);
      var src = anchor.getAttribute("data-figure");
      var caption = anchor.getAttribute("data-figure-label") || "";
      if (current && current !== anchor) current.removeAttribute("aria-describedby");
      current = anchor;
      if (caption) {
        label.textContent = caption;
        label.hidden = false;
      } else {
        label.textContent = "";
        label.hidden = true;
      }
      img.alt = caption || "Figure";
      function reveal() {
        if (current !== anchor) return;
        open(anchor);
      }
      if (img.getAttribute("src") !== src) {
        img.onload = reveal;
        img.onerror = function () {
          if (current === anchor) hide();
        };
        img.src = src;
        if (!img.complete) return;
      }
      reveal();
    }

    function hide() {
      clearTimeout(hideTimer);
      if (current) current.removeAttribute("aria-describedby");
      current = null;
      pinned = false;
      keyboardOpen = false;
      popup.classList.remove("is-open");
      popup.classList.remove("is-above");
      popup.setAttribute("aria-hidden", "true");
    }

    function scheduleHide() {
      clearTimeout(hideTimer);
      hideTimer = setTimeout(function () {
        if (pinned) return;
        if (popup.matches(":hover")) return;
        if (current && current.matches(":hover")) return;
        if (keyboardOpen && current === document.activeElement) return;
        hide();
      }, 80);
    }

    for (var i = 0; i < triggers.length; i++) {
      (function (el) {
        var preload = new Image();
        preload.src = el.getAttribute("data-figure");
        el.addEventListener("mouseenter", function () {
          if (tapMode() && pinned) return;
          pinned = false;
          keyboardOpen = false;
          show(el);
        });
        el.addEventListener("mouseleave", function (event) {
          if (pinned) return;
          if (event.relatedTarget && popup.contains(event.relatedTarget)) return;
          scheduleHide();
        });
        el.addEventListener("focus", function () {
          if (!keyboard) return;
          keyboard = false;
          keyboardOpen = true;
          show(el);
        });
        el.addEventListener("blur", function () {
          keyboardOpen = false;
          if (pinned) return;
          scheduleHide();
        });
        el.addEventListener("pointerdown", function () {
          el._previewTap = tapMode() && current !== el;
        });
        el.addEventListener("click", function (event) {
          if (!tapMode() || !el._previewTap) return;
          event.preventDefault();
          pinned = true;
          keyboardOpen = false;
          show(el);
        });
      })(triggers[i]);
    }

    popup.addEventListener("mouseenter", function () {
      clearTimeout(hideTimer);
    });
    popup.addEventListener("mouseleave", function (event) {
      if (pinned) return;
      if (event.relatedTarget && current && current.contains(event.relatedTarget)) return;
      scheduleHide();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Tab") keyboard = true;
      if (event.key === "Escape") hide();
    });

    document.addEventListener("pointerdown", function (event) {
      if (!pinned) return;
      if (popup.contains(event.target)) return;
      if (current && current.contains(event.target)) return;
      hide();
    });

    document.addEventListener("scroll", function () {
      if (!popup.classList.contains("is-open") && !current) return;
      if (Date.now() - shownAt < 120) {
        if (current) place(current);
        return;
      }
      hide();
    }, true);

    window.addEventListener("resize", function () {
      if (current && popup.classList.contains("is-open")) place(current);
    });
  })();
</script>
</div>
