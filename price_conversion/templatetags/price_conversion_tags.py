from django import template

import requests

register = template.Library()


@register.filter
def convert_english_number_to_persian(number):
    number = str(number)
    english_digits = '1234567890'
    persian_digits = '۱۲۳۴۵۶۷۸۹۰'
    persian_number_table = "".maketrans(english_digits, persian_digits)
    return number.translate(persian_number_table)


@register.filter
def convert_price_to_dollar(number):
    response = requests.get("https://dapi.p3p.repl.co/api/?currency=usd")
    dict_response = response.json()
    return int(dict_response["Price"]) * (number * 10)
