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
      <span class="work-dates">{{ job.dates }}</span>
      <span>{{ job.place }}</span>
    </li>
    {% endfor %}
  </ul>
</div>
