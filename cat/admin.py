from django.contrib import admin
from models import MuseumObject, FunctionalCategory, Person, Place
from models import CulturalBloc, ArtefactType, Region, Category, Maker
from mediaman.models import ArtefactRepresentation
from common.admin import UndeleteableModelAdmin
from cat.adminactions import merge_selected, add_to_collection


class ArtefactRepInline(admin.TabularInline):
    model = ArtefactRepresentation
    search_fields = ['name', ]
#    classes = ('collapse closed',)


class MOAdmin(UndeleteableModelAdmin):
    list_display = ('registration_number', 'cultural_bloc',
                    'description', 'comment',)
    actions = [add_to_collection]

    list_filter = ('place__country', 'functional_category__name',
                    'access_status', 'loan_status', 'cultural_bloc',
                    'artefact_type', 'collector__name', 'donor__name')

    search_fields = ['registration_number', 'description', 'comment',
                     'donor__name', 'collector__name', 'maker__name']

    inlines = [
            ArtefactRepInline,
    ]

    raw_id_fields = ('category', 'place', 'collector', 'collector_2',
            'donor', 'donor_2', 'artefact_type', 'maker')
#    related_lookup_fields = {
#            'fk': ['collector'],
#    }
    autocomplete_lookup_fields = {
            'fk': ['place', 'collector', 'donor', 'artefact_type',
                   'maker'],
            'm2m': ['category']
    }
    filter_horizontal = ['related_documents']

    fieldsets = (
        (None, {
            'fields': ('registration_number', 'old_registration_number',
                       'other_number', 'functional_category', 'artefact_type',
                       'category', 'cultural_bloc', 'place')
        }),
        ('Status', {
            'classes': ('collapse',),
            'fields': (('loan_status', 'access_status'),)
        }),
        ('Storage location', {
            'classes': ('collapse',),
            'fields': (('storage_section', 'storage_unit',),
                ('storage_bay', 'storage_shelf_box_drawer'),)
        }),
        ('Acquisition', {
            'classes': ('collapse',),
            'fields': ('acquisition_date', 'acquisition_method',
                       'reg_info')
        }),
        ('Collector', {
            'classes': ('collapse',),
            'fields': ('collector', 'collector_2',
                'how_collector_obtained', 'when_collector_obtained')
        }),
        ('Donor', {
            'classes': ('collapse',),
            'fields': ('donor', 'donor_2',
                'how_donor_obtained', 'when_donor_obtained')
        }),
        ('Details', {
            'classes': ('collapse',),
            'fields': ('description', 'is_public_comment',
                'comment', 'significance')
        }),
        ('Extra details', {
            'fields': ('maker', 'manufacture_technique', 'creation_date',
                'site_name_number', 'raw_material', 'indigenous_name',
                'recorded_use', 'assoc_cultural_group',
                'exhibition_history')
        }),
        ('Location', {
            'classes': ('collapse',),
            'fields': ('longitude', 'latitude')
        }),
        ('Dimensions', {
            'classes': ('collapse',),
            'fields': (('length', 'width', 'height'),
                ('depth', 'circumference'))
        }),
        ('Related documents', {
            'classes': ('collapse',),
            'fields': ('related_documents',)
        }),
    )


admin.site.register(MuseumObject, MOAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'comments',)
    search_fields = ['name', 'comments']
    filter_horizontal = ['related_documents']
    actions = [merge_selected]
admin.site.register(Person, PersonAdmin)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'region', 'australian_state',
            'name', 'gn_name')
    list_filter = ('country', 'australian_state', 'region',)

    def geocode_place(modeladmin, request, queryset):
        from cat.tasks import GeocodePlace
        for place in queryset:
            GeocodePlace.delay(place.id)
    geocode_place.short_description = "Lookup latitude/longitude"

    def geocode_local(modeladmin, request, queryset):
        pass

    actions = [merge_selected, geocode_place]
    search_fields = ['country', 'region__name', 'australian_state', 'name']
admin.site.register(Place, PlaceAdmin)


class FunctionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition')
    search_fields = ['name']
    actions = [merge_selected]
admin.site.register(FunctionalCategory, FunctionCategoryAdmin)


class CulturalBlocAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition')
    search_fields = ['name', ]
    actions = [merge_selected]
admin.site.register(CulturalBloc, CulturalBlocAdmin)


class ArtefactRepresentationAdmin(admin.ModelAdmin):
    actions = [merge_selected]
    raw_id_fields = ('artefact',)
admin.site.register(ArtefactRepresentation, ArtefactRepresentationAdmin)


class ArtefactTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition', 'see_also')
    search_fields = ['name']
    actions = [merge_selected]
admin.site.register(ArtefactType, ArtefactTypeAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']
admin.site.register(Region, RegionAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'slug')
admin.site.register(Category, CategoryAdmin)


class MakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')
    search_fields = ('name', 'comment')
admin.site.register(Maker, MakerAdmin)
