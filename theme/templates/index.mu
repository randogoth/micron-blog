{% extends "base.mu" %}
{% block content %}
{% block content_title %}
{% endblock %}
{% for article in articles %}
+ [{{ article.locale_date }}] `!`_`[{{ article.title }}`:/page/{{ article.url }}]`_`!

{% endfor %}

{% include 'pagination.mu' %}
{% endblock content %}
