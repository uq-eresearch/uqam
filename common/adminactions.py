import copy
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib import messages
from cat.modelmerge import merge_model_objects
from django.shortcuts import render
from django.contrib import admin


def add_to_collection(modeladmin, request, queryset):
    """
    Provide an action to add selected objects to existing collection
    """
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect(
            "/collection/add_objects?ids=%s" % ",".join(selected))

add_to_collection.short_description = "Add to collection"


def merge_selected(modeladmin, request, queryset):
    """
    Provide the admin action for merging models

    From:
    http://djangosnippets.org/snippets/2213/
    """
    model = queryset.model
    model_name = model._meta.object_name
    return_url = "."
    list_display = copy.deepcopy(modeladmin.list_display)
    ids = []

    if '_selected_action' in request.POST:
        # List of PKs of the selected models
        ids = request.POST.getlist('_selected_action')

# This is passed in for specific merge links.
# This id comes from the linking model (Person, ...)
    if 'id' in request.GET:
        id = request.GET.get('id')
        ids.append(id)
        try:
            queryset = queryset | model.objects.filter(pk=id)
        except AssertionError:
            queryset = model.objects.filter(pk__in=ids)
        return_url = model.objects.get(pk=id).get_absolute_url() or "."

    if 'return_url' in request.POST:
        return_url = request.POST['return_url']

    if 'master' in request.POST:
        master = model.objects.get(id=request.POST['master'])
        queryset = model.objects.filter(pk__in=ids)
        for q in queryset.exclude(pk=master.pk):
            merge_model_objects(master, q)
        # self.message_user(request, "Merged Successfully")
        messages.success(request, "All " + model_name
                + " records have been merged into the selected "
                + model_name + ".")
        return HttpResponseRedirect(return_url)

    #Build the display_table... This is just for the template.
    #----------------------------------------
    display_table = []
    try:
        list_display.remove('action_checkbox')
    except ValueError:
        pass

    from django.forms.forms import pretty_name
    titles = []
    for ld in list_display:
        if hasattr(ld, 'short_description'):
            titles.append(pretty_name(ld.short_description))
        elif hasattr(ld, 'func_name'):
            titles.append(pretty_name(ld.func_name))
        elif ld == "__str__":
            titles.append(model_name)
        else:
            titles.append(ld)
    display_table.append(titles)

    for q in queryset:
        row = []
        for ld in list_display:
            if callable(ld):
                row.append(mark_safe(ld(q)))
            elif ld == "__str__":
                row.append(q)
            else:
                row.append(mark_safe(getattr(q, ld)))
        display_table.append(row)
        display_table[-1:][0].insert(0, q.pk)
    #----------------------------------------

    return render(request, 'merge_preview.html',
            {'queryset': queryset,
                'model': model, 'return_url': return_url,
        'display_table': display_table, 'ids': ids})

merge_selected.short_description = "Merge selected records"
