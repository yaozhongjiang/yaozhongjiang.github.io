---
permalink: /publication/
title: "publication"
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
  <h1 class="page-heading">publication</h1>

  <p class="profile-links">
    {% if site.author.dblp %}
      <a href="{{ site.author.dblp }}">DBLP</a>
    {% endif %}
    {% if site.author.googlescholar %}
      <a href="{{ site.author.googlescholar }}">Google Scholar</a>
    {% endif %}
    {% if site.author.linkedin %}
      <a href="https://www.linkedin.com/in/{{ site.author.linkedin }}">LinkedIn</a>
    {% endif %}
  </p>

  <div class="two-col stat-grid">
    <section class="panel">
      <h2>Papers</h2>
      <p><strong>Journal papers</strong> {{ journal_count }}</p>
      <p><strong>Conference papers</strong> {{ conference_count }}</p>
      <p><strong>Preprints</strong> {{ preprint_count }}</p>
    </section>
    <section class="panel">
      <h2>Citations</h2>
      <p><strong>Citations</strong> {{ site.data.publications.stats.citations }}</p>
      <p><strong>h-index</strong> {{ site.data.publications.stats.h_index }}</p>
      <p><strong>i10-index</strong> {{ site.data.publications.stats.i10_index }}</p>
    </section>
  </div>
  <p class="stat-note">Citation totals are OpenAlex counts for the papers listed here (ORCID {{ site.author.orcid }}). A dash means no citation count was found. Google Scholar did not return numbers.</p>

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
