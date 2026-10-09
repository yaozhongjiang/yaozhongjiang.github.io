---
permalink: /project/
title: "Project"
excerpt: ""
author_profile: false
---

<div class="site-wrap">
  <h1 class="page-heading">Project</h1>
  <p class="contact-note">Public repositories of the <a href="https://github.com/OCTPRISM">OCTPRISM</a> organization.</p>
  <ul class="work-list">
    {% for project in site.data.projects.items %}
    <li>
      <div class="work-head">
        <span class="work-text">
          <a class="project-name" href="{{ project.url }}">{{ project.name }}</a>
        </span>
      </div>
      <div class="work-detail">
        <p><span class="work-label">About</span><span class="work-copy">{{ project.about }}</span></p>
        {% if project.highlight %}
        <p><span class="work-label">Highlight</span><span class="work-copy">{{ project.highlight }}</span></p>
        {% endif %}
      </div>
    </li>
    {% endfor %}
  </ul>
  <p class="project-close">I welcome a conversation about collaboration. Please get in touch through the <a href="{{ '/contact/' | relative_url }}" target="_self">Contact</a> page.</p>
</div>
