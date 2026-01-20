# Project Log

Generated: {{ generation_date }}
Repository: {{ repo_path }}

**Total Items:** {{ total_items }} ({{ total_commits }} commits, {{ total_tests }} tests)

---

{% for item in items %}
![[{{ item.path }}]]
{% endfor %}
