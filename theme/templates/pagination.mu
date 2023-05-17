{% if DEFAULT_PAGINATION %}
-
{% if articles_page.has_previous() %}`[<<`:/{{ articles_previous_page.url }}] {% endif %}Page {{ articles_page.number }} / {{ articles_paginator.num_pages }}{% if articles_page.has_next() %} `[>>`:/{{ articles_next_page.url }}]{% endif %}

{% endif %}
