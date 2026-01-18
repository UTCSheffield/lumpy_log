# Project Log

Generated: {{ generation_date }}
Repository: {{ repo_path }}

**Total Items:** {{ total_items }} ({{ total_commits }} commits, {{ total_tests }} tests)

---

{% for item in items %}
{% if item.type == 'commit' %}
![[{{ item.path }}]]
{% elif item.type == 'test' %}
![[{{ item.path }}]]
{% endif %}

{% endfor %}
