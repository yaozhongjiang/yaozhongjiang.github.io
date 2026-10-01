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
    <img class="home-avatar" src="{{ '/images/yaozhongjiang.jpg' | relative_url }}" alt="{{ site.author.name }}">
    <div class="home-bio">
      <h1>{{ site.author.name }}</h1>
      <p class="home-affiliation">{{ site.author.bio }}</p>
      <p>I obtained my Ph.D. from the University of Chinese Academy of Sciences under the supervision of Professor Jingguo Ge. During my Ph.D. studies, I primarily focused on network traffic identification and tracking. After graduation, I worked at Huawei, where I had the opportunity to participate in projects related to information retrieval, which sparked my interest in LLM-based Agents, natural language processing, and large language models (LLMs). I am currently a postdoctoral researcher at King's College London, where I mainly conduct research in the field of large models. To date, I have published more than 10 papers in areas such as deep learning and LLMs, and I have served as a session chair or reviewer for several international conferences, including IJCNN and CIKM.</p>
      <p>My research fields involve：</p>
      <ul>
        <li>Large Model Agents Collaboration</li>
        <li>LLM performance and security evaluation</li>
        <li>Natural Language Processing</li>
        <li>Blockchain</li>
        <li>Traffic Classification</li>
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
