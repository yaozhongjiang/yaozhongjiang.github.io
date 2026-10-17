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
      <p class="home-role">Research Fellow</p>
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
      <p markdown="span">I am a **Postdoctoral Researcher at King's College London**, working under the supervision of **Dr. Yali Du**. My research focuses on **Multi-Agent Systems and Large Language Model (LLM) Security**, with particular interests in multi-agent collaboration, agent coordination, and the security and trustworthiness of LLM-based systems.</p>
      <p markdown="span">I received my Ph.D. from the **University of Chinese Academy of Sciences (UCAS)**, where my research focused on network traffic identification and tracking. I subsequently worked on information retrieval at **Huawei**, which led to my broader research interests in natural language processing and large language models.</p>
      <p markdown="span">I have published **over ten research papers** in deep learning and large language models. I actively contribute to the research community as a **Senior Program Committee (SPC) member of AAMAS** and a reviewer for leading conferences, including **ICLR and ACL**.</p>
    </div>
  </div>

  <div class="two-col">
    <section class="panel">
      <h2>Recent activities</h2>
      <ul class="activity-list">
        {% for item in site.data.activities.items %}
        <li data-end="{{ item.end }}"{% if item.done %} data-done="true"{% endif %}>
          <span class="activity-date">{{ item.date }}</span>
          <span class="activity-body">
            {% if item.logos %}
            <span class="activity-logos">
              {% for logo in item.logos %}
              <img src="{{ logo.src | relative_url }}" alt="{{ logo.alt }}">
              {% endfor %}
            </span>
            {% endif %}
            <span class="activity-copy">{{ item.text }}<span class="activity-check" aria-hidden="true"></span></span>
          </span>
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
            var finished = items[i].getAttribute("data-done") === "true" || items[i].getAttribute("data-end") < today;
            if (!finished) continue;
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
        {% assign latest_year = site.data.publications.papers | map: "year" | sort | last %}
        {% for paper in site.data.publications.papers %}
          {% if paper.year == latest_year %}
          <li>
            <span class="paper-year">{{ paper.year }}</span>
            {% if paper.url != "" %}
              <a href="{{ paper.url }}">{{ paper.title }}</a>
            {% else %}
              {{ paper.title }}
            {% endif %}
          </li>
          {% endif %}
        {% endfor %}
      </ul>
    </section>
  </div>
</div>
