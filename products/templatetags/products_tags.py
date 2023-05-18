from django import template

import html

register = template.Library()


@register.filter
def replace_dash_with_space_category_name(category_name):
    category_name = html.unescape(category_name)
    return category_name.replace("-", " ")
