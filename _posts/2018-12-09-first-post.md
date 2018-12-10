---
layout: post
title:  First Post
date:   2018-12-09 20:00:09 +0100
categories: jekyll test
---

<body>
{% for file in site.static_files %}
  {% if file.image %}
    <img src="{{file.path}}" alt="{{file.name}}">
  {% endif %}
{% endfor %}
<\body>
