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
      {% if job.logo %}
        <img class="work-logo" src="{{ job.logo | relative_url }}" alt="{{ job.logo_alt }}">
      {% endif %}
      <span class="work-text">
        <span class="work-dates">{{ job.dates }}</span>
        <span>{{ job.place }}</span>
      </span>
    </li>
    {% endfor %}
  </ul>
</div>
