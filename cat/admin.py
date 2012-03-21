from django.contrib import admin
from models import MuseumObject, FunctionalCategory
from models import CulturalBloc, ArtefactType, Category
from models import AcquisitionMethod, LoanStatus
from models import AccessStatus, Obtained
from models import PhotoType
from mediaman.models import ArtefactRepresentation
from common.admin import UndeleteableModelAdmin
from common.adminactions import merge_selected, add_to_collection


class ArtefactRepInline(admin.TabularInline):
    model = ArtefactRepresentation
    search_fields = ['name', ]
#    classes = ('collapse closed',)


class MOAdmin(UndeleteableModelAdmin):
    list_display = ('registration_number',
                    'description', 'comment',)
    actions = [add_to_collection]

    list_filter = ('place__country', 'functional_category__name',
                    'access_status', 'loan_status', 'cultural_bloc',
                    'artefact_type', 'collector', 'donor')

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
                       'other_number', 'functional_category', 'category',
                       'artefact_type', 'cultural_bloc', 'place')
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
                'comment', 'private_comment', 'significance')
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


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'slug')
    actions = [merge_selected]
admin.site.register(Category, CategoryAdmin)


class AcquisitionMethodAdmin(admin.ModelAdmin):
    actions = [merge_selected]
admin.site.register(AcquisitionMethod, AcquisitionMethodAdmin)


class LoanStatusAdmin(admin.ModelAdmin):
    actions = [merge_selected]
admin.site.register(LoanStatus, LoanStatusAdmin)


class AccessStatusAdmin(admin.ModelAdmin):
    actions = [merge_selected]
admin.site.register(AccessStatus, AccessStatusAdmin)


class ObtainedAdmin(admin.ModelAdmin):
    actions = [merge_selected]
admin.site.register(Obtained, ObtainedAdmin)


class PhotoTypeAdmin(admin.ModelAdmin):
    actions = [merge_selected]
admin.site.register(PhotoType, PhotoTypeAdmin)

