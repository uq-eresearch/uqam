from django.contrib import admin
from models import MuseumObject, FunctionalCategory, Person, Place
from models import CulturalBloc, ArtefactType, Region
from mediaman.models import ArtefactRepresentation
from common.admin import UndeleteableModelAdmin
from cat.adminactions import merge_selected, add_to_collection

class ArtefactRepInline(admin.TabularInline):
    model = ArtefactRepresentation
    classes = ('collapse closed',)



class MOAdmin(UndeleteableModelAdmin):
    list_display = ('registration_number','cultural_bloc','description','comment',)
    actions = [add_to_collection]

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



class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'comments',)
    search_fields = ['name', 'comments',]
    filter_horizontal = ['related_documents']
    actions = [merge_selected]
admin.site.register(Person, PersonAdmin)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'region', 'australian_state', 'name',)
    list_filter = ('country', 'australian_state', 'region',)
    actions = [merge_selected]
    search_fields = ['country', 'region__name','australian_state', 'name']
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

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
admin.site.register(Region, RegionAdmin)
