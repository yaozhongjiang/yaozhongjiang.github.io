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
      {% if site.author.linkedin contains "://" %}
        {% assign linkedin_url = site.author.linkedin %}
      {% else %}
        {% assign linkedin_url = "https://www.linkedin.com/in/" | append: site.author.linkedin %}
      {% endif %}
      <a href="{{ linkedin_url }}"><img class="brand-icon" src="{{ '/images/logos/linkedin.svg' | relative_url }}" alt="" width="18" height="18"> LinkedIn</a>
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
  <p class="stat-note">Lines show papers and citation counts by publication year. A year with no papers or citations is drawn as zero. Totals use OpenAlex (ORCID {{ site.author.orcid }}). Google Scholar did not return numbers.</p>
  <script id="yearly-data" type="application/json">{{ site.data.publications.yearly | jsonify }}</script>
  <script src="{{ '/assets/js/year-charts.js' | relative_url }}"></script>

  <div class="pub-table-wrap">
    <table class="pub-table">
      <thead>
        <tr>
          <th class="num">#</th>
          <th>Title</th>
          <th>Venue</th>
          <th class="num">Year</th>
          <th class="num">Citations</th>
        </tr>
      </thead>
      <tbody>
        {% for paper in site.data.publications.papers %}
        <tr>
          <td class="num">{{ forloop.index }}</td>
          <td>
            {% if paper.url != "" %}
              <a href="{{ paper.url }}">{{ paper.title }}</a>
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
</div>
