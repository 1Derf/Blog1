from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary is None:  # Handle None gracefully
        return None
    return dictionary.get(key)