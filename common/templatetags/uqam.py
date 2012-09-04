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
def advanced_search_fields(form=None):
    categories = Category.objects.all().order_by('name')
    global_regions = GlobalRegion.objects.all()

    selected_category = None
    selected_global_region = None
    if form and form.is_valid():
        if form.cleaned_data['category']:
            selected_category = form.cleaned_data['category'][0]
        if form.cleaned_data['global_region']:
            selected_global_region = form.cleaned_data['global_region'][0]


    return {
        'categories': categories,
        'global_regions': global_regions,
        'form': form,
        'selected_category': selected_category,
        'selected_global_region': selected_global_region
    }
