# lang: {{ DEFAULT_LANG }}
{% block head %}
> {% block title %}{{ SITENAME }}{% endblock title %}
{% endblock head %}

{% for title, link in MENUITEMS %}`[{{ title }}`{{ link }}]{% endfor %}{% if DISPLAY_PAGES_ON_MENU %}{% for p in PAGES %}`[{{ p.title }}`/{{ p.url }}]{% endfor %}{% else %}{% if DISPLAY_CATEGORIES_ON_MENU %}{% for cat, null in categories %}`[{% if cat == category %}`_{% endif %}{{ cat }}{% if cat == category %}`_{% endif %}`/{{ cat.url }}]{% endfor %}{% endif %}{% endif %}

{% block content %}
{% endblock %}

{% if DESCRIPTION %}
{{ DESCRIPTION }}
{% endif %}