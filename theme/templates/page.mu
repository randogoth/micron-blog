{% extends "base.mu" %}
{% block title %}{{ page.title }}{%endblock%}
{% block content %}
>{{ page.title }}
{% import 'translations.html' as translations with context %}
{{ translations.translations_for(page) }}
{{ page.content }}
{% endblock %}
