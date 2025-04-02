from django import template

register = template.Library()

@register.filter
def dict_contains(dictionary, key):
    return key in dictionary

@register.filter
def get_id(dictionary, key):
    return key in dictionary