{% extends "base.mu" %}
{% block content %}
{% block content_title %}
{% endblock %}

{% for article in articles %}

+[{{ article.locale_date }}]
>>>>`[`!{{ article.title }}`!`/{{ article.url }}]
>>>>{{ article.summary }}

-

{% endfor %}

{% include 'pagination.mu' %}
{% endblock content %}
