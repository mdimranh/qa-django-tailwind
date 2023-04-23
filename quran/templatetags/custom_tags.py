import convert_numbers
from django import template
import re

register = template.Library()

def english_to_bengali(value):
    val = str(value).replace("0", "০").replace("1", "১").replace("2", "২").replace("3", "৩").replace("4", "৪").replace("5", "৫").replace("6", "৬").replace("7", "৭").replace("8", "৮").replace("9", "৯")
    return val

functions = {
    "english_to_arabic": convert_numbers.english_to_arabic,
    "english_to_bengali": english_to_bengali
}

# An upper function that capitalizes word passed to it. We then register the filter using a suitable name.
@register.simple_tag
def number_convert(function, value):
  return functions[function](value)

@register.simple_tag
def make_3_digit(value):
    if len(value) == 3:
        return value
    elif len(value) == 2:
        return f"0{value}"
    elif len(value) == 1:
        return f"00{value}"
