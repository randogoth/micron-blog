{% extends "base.mu" %}
{% block content %}
>Archives for {{ period | reverse | join(' ') }}

{% for article in dates %}
+[{{ article.locale_date }}]
>>>>`[`!{{ article.title }}`!`:/{{ article.url }}]
>>>>{{ article.summary }}
{% endfor %}
{% endblock %}
