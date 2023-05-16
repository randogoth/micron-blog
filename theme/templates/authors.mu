{% extends "base.mu" %}
{% block content %}
>Authors on {{ SITENAME }}

{%- for author, articles in authors|sort %}
+ `[{{ author }}`/{{ author.url }}] ({{ articles|count }})

{% endfor %}
{% endblock %}
