---
permalink: /work/
title: "Work"
excerpt: ""
author_profile: false
---

<div class="site-wrap">
  <h1 class="page-heading">Work</h1>
  <ul class="work-list">
    {% for job in site.data.work.items %}
    <li>
      <div class="work-head">
        {% if job.logo %}
          <img class="work-logo" src="{{ job.logo | relative_url }}" alt="{{ job.logo_alt }}">
        {% endif %}
        <span class="work-text">
          <span class="work-dates">{{ job.dates }}</span>
          <span>{{ job.place }}</span>
        </span>
      </div>
      <div class="work-detail">
        {% if job.focus %}
        <p><span class="work-label">Focus</span> {{ job.focus }}</p>
        {% endif %}
        {% if job.contribution %}
        <p><span class="work-label">Contribution</span> {{ job.contribution }}</p>
        {% endif %}
        {% if job.awards %}
        <p><span class="work-label">Awards</span> {{ job.awards }}</p>
        {% endif %}
      </div>
    </li>
    {% endfor %}
  </ul>

  <h2>Patents</h2>
  <p class="stat-note">Invention applications that list Zhongjiang Yao as an inventor. The year is the filing year.</p>
  <div class="pub-table-wrap">
    <table class="pub-table">
      <thead>
        <tr>
          <th>Title</th>
          <th>Number</th>
          <th>Applicant</th>
          <th class="num">Year</th>
        </tr>
      </thead>
      <tbody>
        {% for patent in site.data.work.patents %}
        <tr>
          <td>{% if patent.url %}<a href="{{ patent.url }}">{{ patent.title }}</a>{% else %}{{ patent.title }}{% endif %}</td>
          <td>{{ patent.number }}</td>
          <td>{{ patent.applicant }}</td>
          <td class="num">{{ patent.year }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
