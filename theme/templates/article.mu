{% extends "base.mu" %}
{% block content %}
>{{ article.title }}
{% import 'translations.mu' as translations with context %}
{{ translations.translations_for(article) }}
{{ article.locale_date }} {% if article.authors %}by {% for author in article.authors %}{{ author }}{% endfor %}{% endif %}
 
 
{{ article.content }}

{% endblock %}
