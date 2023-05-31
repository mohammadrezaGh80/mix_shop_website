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
    response = requests.get("http://api.navasan.tech/latest?api_key=freet5OQhAkh5Z3UpIWRcl4b65brHfpm&item=usd_buy")
    dict_response = response.json()
    converted_number = number / int(dict_response["usd_buy"]["value"])
    return converted_number if converted_number > 1 else 1
