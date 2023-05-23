{% extends "base.mu" %}
{% block content %}
{% for category, articles in categories %}
+ `[{{ category }}`:/page/{{ category.url }}]
{% endfor %}
{% endblock %}
