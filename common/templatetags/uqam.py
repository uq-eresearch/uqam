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


@register.filter
def pdb(element):
    """
    Inside a template do {{ template_var|pdb }}
    """
    import ipdb
    ipdb.set_trace()
    return element


from cat.models import Category
from location.models import GlobalRegion


@register.inclusion_tag('snippets/advanced_search_fields.html')
def advanced_search_fields():
    categories = Category.objects.all().order_by('name')
    places = GlobalRegion.objects.all()

    return {
        'categories': categories,
        'places': places,
    }
