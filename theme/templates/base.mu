# lang: {{ DEFAULT_LANG }}
{% block head %}
> {% block title %}{{ SITENAME }}{% endblock title %}
{% endblock head %}

{% for title, link in MENUITEMS %}`[{{ title }}`{{ link }}]{% endfor %}{% if DISPLAY_PAGES_ON_MENU %}{% for p in PAGES %}`[{{ p.title }}`:/page/{{ p.url }}]{% endfor %}{% endif %}

{% block content %}
{% endblock %}

{% if DESCRIPTION %}
{{ DESCRIPTION }}
{% endif %}