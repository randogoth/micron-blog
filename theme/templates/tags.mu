{% extends "base.mu" %}
{% block content %}
{% for tag, articles in tags %}
+ `[{{ tag }}`:/page/{{ tag.url }}]
{% endfor %}
{% endblock %}
