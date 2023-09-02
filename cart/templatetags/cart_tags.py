from django import template

register = template.Library()


@register.filter
def multiply(first_number, second_number):
    return first_number * second_number
