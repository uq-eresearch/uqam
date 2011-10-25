from django.contrib import admin
from models import MuseumObject, FunctionalCategory, Person, Place
from models import CulturalBloc, ArtefactType
from mediaman.models import ArtefactRepresentation

class ArtefactRepInline(admin.TabularInline):
    model = ArtefactRepresentation
    classes = ('collapse closed',)

class MOAdmin(admin.ModelAdmin):
    list_display = ('registration_number','cultural_bloc','description','comment',)

    list_filter = ('place__country','functional_category__name', 'access_status', 'loan_status', 'cultural_bloc',)

    search_fields = ['registration_number', 'description','comment']

    inlines = [
            ArtefactRepInline,
    ]

#    raw_id_fields = ('collector',)
#    related_lookup_fields = {
#            'fk': ['collector'],
#    }
#    autocomplete_lookup_fields = {
#            'fk': ['artefact_type'],
#    }
    filter_horizontal = ['related_documents']

    fieldsets = (
        (None, {
            'fields': ('registration_number', 'old_registration_number',
                       'other_number', 'functional_category', 'artefact_type',
                       'cultural_bloc', 'place')
        }),
        ('Status', {
            'classes': ('collapse',),
            'fields': (('loan_status', 'access_status'),)
        }),
        ('Storage location', {
            'classes': ('collapse',),
            'fields': (('storage_section', 'storage_unit',), ('storage_bay', 'storage_shelf_box_drawer'),)
        }),
        ('Acquisition', {
            'classes': ('collapse',),
            'fields': ('acquisition_date', 'acquisition_method')
        }),
        ('Collector', {
            'classes': ('collapse',),
            'fields': ('collector', 'collector_2', 'how_collector_obtained', 'when_collector_obtained')
        }),
        ('Donor', {
            'classes': ('collapse',),
            'fields': ('donor', 'donor_2', 'how_donor_obtained', 'when_donor_obtained')
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('description', 'comment')
        }),
        ('Extra details', {
            'fields': ('maker_or_artist', 'site_name_number', 'raw_material',
                       'indigenous_name', 'recorded_use', 'assoc_cultural_group')
        }),
        ('Location', {
            'classes': ('collapse closed',),
            'fields': ('longitude', 'latitude')
        }),
        ('Dimensions', {
            'classes': ('collapse closed',),
            'fields': (('length', 'width', 'height'), ('depth', 'circumference'))
        }),
        ('Related documents', {
            'classes': ('collapse closed',),
            'fields': ('related_documents',)
        }),
    )



admin.site.register(MuseumObject, MOAdmin)


def merge_selected(modeladmin,request,queryset): #This is an admin/
    """
    Provide the admin action for merging models

    From:
    http://djangosnippets.org/snippets/2213/
    """
    import copy
    from django.http import HttpResponseRedirect
    from django.utils.safestring import mark_safe
    from django.contrib import messages
    from cat.modelmerge import merge_model_objects
    from django.shortcuts import render_to_response
    from django.template import RequestContext
    model = queryset.model
    model_name = model._meta.object_name
    return_url = "."
    list_display = copy.deepcopy(modeladmin.list_display)
    ids = []

    if '_selected_action' in request.POST: #List of PK's of the selected models
        ids = request.POST.getlist('_selected_action')

    if 'id' in request.GET: #This is passed in for specific merge links. This id comes from the linking model (Person, ...)
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
            merge_model_objects(master,q)
        messages.success(request,"All " + model_name + " records have been merged into the selected " + model_name + ".")
        return HttpResponseRedirect(return_url)

    #Build the display_table... This is just for the template.
    #----------------------------------------
    display_table = []
    try: list_display.remove('action_checkbox')
    except ValueError: pass

    from django.forms.forms import pretty_name
    titles = []
    for ld in list_display:
        if hasattr(ld,'short_description'):
            titles.append(pretty_name(ld.short_description))
        elif hasattr(ld,'func_name'):
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
                row.append(mark_safe(getattr(q,ld)))
        display_table.append(row)
        display_table[-1:][0].insert(0,q.pk)
    #----------------------------------------

    return render_to_response('merge_preview.html',{'queryset': queryset,
                                                    'model': model, 'return_url':return_url,
                                                    'display_table':display_table, 'ids': ids},
                              context_instance=RequestContext(request))

merge_selected.short_description = "Merge selected records"

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'comments',)
    search_fields = ['name', 'comments',]
    filter_horizontal = ['related_documents']
    actions = [merge_selected]
admin.site.register(Person, PersonAdmin)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('country', 'region', 'australian_state', 'name',)
    list_filter = ('country', 'australian_state', 'region',)
    actions = [merge_selected]
admin.site.register(Place, PlaceAdmin)

class FunctionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition')
    actions = [merge_selected]
admin.site.register(FunctionalCategory, FunctionCategoryAdmin)

class CulturalBlocAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition')
    actions = [merge_selected]
admin.site.register(CulturalBloc, CulturalBlocAdmin)

class ArtefactRepresentationAdmin(admin.ModelAdmin):
    actions = [merge_selected]
    raw_id_fields = ('artefact',)
admin.site.register(ArtefactRepresentation, ArtefactRepresentationAdmin)

class ArtefactTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition')
    actions = [merge_selected]
admin.site.register(ArtefactType, ArtefactTypeAdmin)
