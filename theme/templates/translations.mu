{% macro translations_for(article) %}
{% if article.translations %}
{% for translation in article.translations %}
`[{{ translation.lang }}`:/{{ translation.url }}]
{% endfor %}
{% endif %}
{% endmacro %}

