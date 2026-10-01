---
permalink: /
title: "Home"
excerpt: ""
author_profile: false
redirect_from:
  - /about/
  - /about.html
---

<div class="site-wrap">
  <div class="home-hero">
    <div class="home-identity">
      <img class="home-avatar" src="{{ '/images/yaozhongjiang.jpg' | relative_url }}" alt="{{ site.author.name }}">
      <h1>{{ site.author.name }}</h1>
      <p class="home-affiliation">{{ site.author.bio }}</p>
      <p class="identity-links">
        {% if site.author.linkedin %}
          {% if site.author.linkedin contains "://" %}
            {% assign linkedin_url = site.author.linkedin %}
          {% else %}
            {% assign linkedin_url = "https://www.linkedin.com/in/" | append: site.author.linkedin %}
          {% endif %}
          <a href="{{ linkedin_url }}" aria-label="LinkedIn"><img src="{{ '/images/logos/linkedin.svg' | relative_url }}" alt="LinkedIn" width="26" height="26"></a>
        {% endif %}
        {% if site.author.orcid %}
          <a href="{{ site.author.orcid }}" aria-label="ORCID"><img src="{{ '/images/logos/orcid.svg' | relative_url }}" alt="ORCID" width="26" height="26"></a>
        {% endif %}
      </p>
    </div>
    <div class="home-bio">
      <p>I obtained my Ph.D. from the University of Chinese Academy of Sciences under the supervision of Professor Jingguo Ge. During my Ph.D. studies, I primarily focused on network traffic identification and tracking. After graduation, I worked at Huawei, where I had the opportunity to participate in projects related to information retrieval, which sparked my interest in LLM-based Agents, natural language processing, and large language models (LLMs). I am currently a postdoctoral researcher at King's College London, where I mainly conduct research in the field of large models. To date, I have published more than 10 papers in areas such as deep learning and LLMs, and I have served as a session chair or reviewer for several international conferences, including IJCNN and CIKM.</p>
      <p>My research fields involve：</p>
      <ul>
        <li>multi agent collaboration</li>
        <li>LLM privacy and security</li>
        <li>Natural Language Processing</li>
        <li>Blockchain</li>
        <li>Traffic Analysis</li>
      </ul>
    </div>
  </div>

  <div class="two-col">
    <section class="panel">
      <h2>Recent activities</h2>
      <ul class="activity-list">
        {% for item in site.data.activities.items %}
        <li>
          <span class="activity-date">{{ item.date }}</span>
          <span>{{ item.text }}</span>
        </li>
        {% endfor %}
      </ul>
    </section>
    <section class="panel">
      <h2>Recently published papers</h2>
      <ul class="recent-papers">
        {% for paper in site.data.publications.papers %}
          {% if paper.recent and paper.url != "" %}
          <li>
            <span class="paper-year">{{ paper.year }}</span>
            <a href="{{ paper.url }}">{{ paper.title }}</a>
          </li>
          {% endif %}
        {% endfor %}
      </ul>
    </section>
  </div>
</div>
