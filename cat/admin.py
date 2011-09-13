from django.contrib import admin
from models import MuseumObject, FunctionalCategory,Person, Place
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

    raw_id_fields = ('collector',)
    related_lookup_fields = {
            'fk': ['collector'],
    }
#    autocomplete_lookup_fields = {
#            'fk': ['artefact_type'],
#    }

    fieldsets = (
        (None, {
            'fields': ('registration_number', 'old_registration_number',
                       'other_number', 'functional_category', 'artefact_type',
                       'cultural_bloc', 'place')
        }),
        ('Status', {
            'fields': ('loan_status', 'access_status')
        }),
        ('Storage location', {
            'fields': ('storage_section', 'storage_unit', 'storage_bay', 'storage_shelf_box_drawer')
        }),
        ('Acquisition', {
            'fields': ('acquisition_date', 'acquisition_method')
        }),
        ('Donor', {
            'fields': ('donor', 'donor_2', 'how_donor_obtained', 'when_donor_obtained')
        }),
        ('Collector', {
            'fields': ('collector', 'how_collector_obtained')
        }),
        ('Details', {
            'fields': ('description', 'comment')
        }),
        ('Extra details', {
            'fields': ('maker_or_artist', 'site_name_number', 'raw_material',
                       'indigenous_name', 'recorded_use', 'assoc_cultural_group')
        }),
        ('Location', {
            'fields': ('longitude', 'latitude')
        }),
        ('Dimensions', {
            'classes': ('collapse closed',),
            'fields': (('length', 'width', 'height'), ('depth', 'circumference'))
        }),
    )



admin.site.register(MuseumObject, MOAdmin)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('country', 'region', 'australian_state', 'name',)
    list_filter = ('country', 'australian_state', 'region',)
admin.site.register(Place, PlaceAdmin)

admin.site.register(FunctionalCategory)
admin.site.register(CulturalBloc)
admin.site.register(ArtefactRepresentation)
admin.site.register(ArtefactType)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'comments',)
    search_fields = ['name', 'comments',]
admin.site.register(Person, PersonAdmin)
