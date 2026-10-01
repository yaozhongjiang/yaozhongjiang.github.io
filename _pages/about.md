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
          {% include linkedin-url.html %}
          <a href="{{ linkedin_url }}" aria-label="LinkedIn" title="https://www.linkedin.com/in/zhongjiang-yao-b0756a406/"><img src="{{ '/images/logos/linkedin.svg' | relative_url }}" alt="LinkedIn" width="26" height="26"></a>
        {% endif %}
        {% if site.author.orcid %}
          <a href="{{ site.author.orcid }}" aria-label="ORCID"><img src="{{ '/images/logos/orcid.svg' | relative_url }}" alt="ORCID" width="26" height="26"></a>
        {% endif %}
      </p>
    </div>
    <div class="home-bio">
      <p>I am a postdoctoral researcher at King's College London. My research centers on multi-agent collaboration and LLM security. I received my Ph.D. from the University of Chinese Academy of Sciences, where I studied network traffic identification and tracking, and I later worked at Huawei on information retrieval. That work led me into natural language processing and large language models. I have published more than ten papers on deep learning and large language models, and I serve as a Senior PC of AAMAS and as a reviewer for ICLR and ACL.</p>
      <p>My research fields involve：</p>
      <ul>
        <li>Multi Agent Collaboration</li>
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
        <li data-end="{{ item.end }}">
          <span class="activity-date">{{ item.date }}</span>
          <span>{{ item.text }}<span class="activity-check" aria-hidden="true"></span></span>
        </li>
        {% endfor %}
      </ul>
      <script>
        (function () {
          var now = new Date();
          var month = now.getMonth() + 1;
          var day = now.getDate();
          var today = now.getFullYear() + "-" + (month < 10 ? "0" : "") + month + "-" + (day < 10 ? "0" : "") + day;
          var items = document.querySelectorAll(".activity-list li[data-end]");
          for (var i = 0; i < items.length; i++) {
            if (items[i].getAttribute("data-end") >= today) continue;
            var mark = items[i].querySelector(".activity-check");
            mark.textContent = "✓";
            mark.setAttribute("aria-label", "Completed");
            mark.removeAttribute("aria-hidden");
          }
        })();
      </script>
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
