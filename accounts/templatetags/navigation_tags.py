"""Template tags for navigation helpers."""

from django import template

register = template.Library()


@register.filter
def startswith(text, prefix):
    """Return True when text starts with prefix."""

    if not isinstance(text, str) or not isinstance(prefix, str):
        return False
    return text.startswith(prefix)
