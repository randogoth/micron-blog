{% extends "base.mu" %}
{% block content %}
{% for category, articles in categories %}
+ `[{{ category }}`:/{{ category.url }}]
{% endfor %}
{% endblock %}
