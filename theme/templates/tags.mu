{% extends "base.mu" %}
{% block content %}
{% for tag, articles in tags %}
+ `[{{ tag }}`/{{ tag.url }}]
{% endfor %}
{% endblock %}
