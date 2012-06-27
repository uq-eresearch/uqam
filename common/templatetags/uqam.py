from django import template

register = template.Library()


@register.filter
def dimension(value, arg):
    """
    Dimension integers

    If value, append arg, otherwise output nothing
    """
    if value:
        return str(value) + " " + arg
    return ""


@register.filter
def verbose_name(obj):
    """
    Return the verbose name of a model
    """
    return obj._meta.verbose_name