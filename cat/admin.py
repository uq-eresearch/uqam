from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from models import MuseumObject, FunctionalCategory
from models import CulturalBloc, ArtefactType, Category
from models import AcquisitionMethod, LoanStatus
from models import AccessStatus, Obtained
from models import PhotoType, RecordStatus
from mediaman.models import ArtefactRepresentation, Document
from common.admin import UndeleteableModelAdmin
from common.adminactions import merge_selected, add_to_collection
from common.adminactions import generate_xls
from admin_views import search_home, search_xls


class ArtefactRepInline(admin.TabularInline):
    model = ArtefactRepresentation
    search_fields = ['name', ]
    fields = ('name', 'image', 'position')
    sortable_field_name = "position"
#    classes = ('collapse closed',)


class DocumentInline(admin.TabularInline):
    model = MuseumObject.related_documents.through
    search_fields = ['name', ]
    raw_id_fields = ('document',)
    autocomplete_lookup_fields = {
            'm2m': ['document']
    }


class MOAdmin(UndeleteableModelAdmin):
    list_display = ('registration_number',
                    'description', 'comment',)
    actions = [add_to_collection, generate_xls]

    list_filter = ('place__country', 'functional_category__name',
                    'access_status', 'loan_status', 'cultural_bloc',
                    'artefact_type', 'collector', 'donor')

    search_fields = ['registration_number', 'description', 'comment',
                     'donor__name', 'collector__name', 'maker__name']

    inlines = [
            DocumentInline, ArtefactRepInline
    ]

    raw_id_fields = ('category', 'place', 'collector', 'collector_2',
            'donor', 'donor_2', 'artefact_type', 'maker')
    autocomplete_lookup_fields = {
            'fk': ['place', 'collector', 'donor', 'artefact_type',
                   'maker'],
            'm2m': ['category']
    }
#    readonly_fields = ('loan_status',)

    fieldsets = (
        (None, {
            'fields': ('registration_number', 'old_registration_number',
                       'other_number', 'functional_category', 'category',
                       'artefact_type', 'cultural_bloc', 'place')
        }),
        ('Status', {
            'classes': ('collapse',),
            'fields': ('loan_status', 'access_status', 'record_status',)
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
                'exhibition_history', 'category_illustrated',
                'artefact_illustrated')
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
    )

    def get_urls(self):
        urls = super(MOAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^search/$', self.admin_site.admin_view(search_home),
                name='search'),
            url(r'^search_results/$', self.admin_site.admin_view(search_home),
                {'template_name': 'common/search_results.html'},
                name='search_results'),
            url(r'^search_xls/$',  self.admin_site.admin_view(search_xls),
                name='search_xls'),
#            (r'^filter/$', self.admin_site.admin_view(self.my_view))
        )
        return my_urls + urls

    def my_view(self, request):
        pass


admin.site.register(MuseumObject, MOAdmin)


class FunctionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'definition')
    fields = ('name', 'definition')
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
    fields = ('name', 'definition', 'see_also')
    search_fields = ['name']
    actions = [merge_selected]
admin.site.register(ArtefactType, ArtefactTypeAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'slug')
    list_display = ('__unicode__', 'description')
    actions = [merge_selected]
admin.site.register(Category, CategoryAdmin)


class AcquisitionMethodAdmin(admin.ModelAdmin):
    list_display = ('method', 'definition')
    fields = ('method', 'preposition', 'definition')
    search_fields = ('method', 'definition')
    actions = [merge_selected]
admin.site.register(AcquisitionMethod, AcquisitionMethodAdmin)


class LoanStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'definition')
    fields = ('status', 'definition')
    search_fields = ('status', 'definition')
    actions = [merge_selected]
admin.site.register(LoanStatus, LoanStatusAdmin)


class AccessStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'definition')
    fields = ('status', 'definition')
    search_fields = ('status', 'definition')
    actions = [merge_selected]
admin.site.register(AccessStatus, AccessStatusAdmin)


class ObtainedAdmin(admin.ModelAdmin):
    list_display = ('how', 'definition')
    fields = ('how', 'definition')
    search_fields = ('how', 'definition')
    actions = [merge_selected]
admin.site.register(Obtained, ObtainedAdmin)


class PhotoTypeAdmin(admin.ModelAdmin):
    list_display = ('phototype', 'definition')
    fields = ('phototype', 'definition')
    search_fields = ('phototype', 'definition')
    actions = [merge_selected]
#TODO: Show this properly with photorecords linked to items
#admin.site.register(PhotoType, PhotoTypeAdmin)


class RecordStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'definition')
    fields = ('status', 'definition')
    search_fields = ('status', 'definition')
    actions = [merge_selected]
admin.site.register(RecordStatus, RecordStatusAdmin)

