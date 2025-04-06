from django import template

register = template.Library()

@register.filter
def split_by(value, delimiter=","):
    """
    Splits the given string by the specified delimiter.
    Returns a list.
    """
    try:
        return value.split(delimiter)
    except AttributeError:
        return []

@register.filter
def trim(value):
    """
    Trims leading and trailing whitespace from the given string.
    """
    try:
        return value.strip()
    except AttributeError:
        return value

@register.filter
def get_range(value):
    """
    Returns a range from 0 to the given value (non-inclusive).
    Useful for iterating a fixed number of times in templates.
    """
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return []
