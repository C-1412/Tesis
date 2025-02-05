# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})