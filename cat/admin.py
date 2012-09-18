from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from models import MuseumObject, FunctionalCategory
from models import CulturalBloc, ArtefactType, Category
from models import AcquisitionMethod, LoanStatus
from models import AccessStatus, Obtained
from models import RecordStatus
from mediaman.models import ArtefactRepresentation
from common.admin import UndeleteableModelAdmin
from common.adminactions import merge_selected, add_to_collection
from common.adminactions import generate_xls, add_to_opener
from admin_views import search_home, search_xls
from django.core import urlresolvers
from django.utils.datastructures import SortedDict
from location.models import Country, StateProvince, RegionDistrict, Locality


class MediaFileInline(admin.TabularInline):
    extra = 0
    search_fields = ['name', ]

    def has_add_permission(self, request):
        return False


class ArtefactRepInline(MediaFileInline):
    model = ArtefactRepresentation
#   position field hidden with CSS
    fields = ('name', 'image', 'thumbnail', 'view_admin_record', 'public', 'position')

    def thumbnail(self, obj):
        try:
            thumb_opts = {'size': (64, 64), 'watermark': ''}
            thumb = obj.image.get_thumbnail(thumb_opts)
            return '<a href="%s"><img src="%s"></a>' % (obj.image.url, thumb.url)
        except:
            return 'Error generating thumbnail'

    def view_admin_record(self, obj):
        try:
            admin_url = urlresolvers.reverse('admin:mediaman_artefactrepresentation_change', args=(obj.id,))
            return '<a href="%s">View image record</a>' % (admin_url,)
        except:
            return ''
    view_admin_record.allow_tags = True
    thumbnail.allow_tags = True
    readonly_fields = ('name', 'image', 'thumbnail', 'view_admin_record')
    sortable_field_name = "position"


class DocumentInline(MediaFileInline):
    model = MuseumObject.related_documents.through
    fields = ('view_document', 'admin_doc_link', 'is_public')
    readonly_fields = ('view_document', 'admin_doc_link', 'is_public')

    def is_public(self, obj):
        return obj.document.public
    is_public.boolean = True

    def view_document(self, obj):
        try:
            doc = obj.document.document
            return '<a href="%s">%s</a>' % (doc.url, doc.name)
        except:
            return ''

    def admin_doc_link(self, obj):
        try:
            doc = obj.document
            admin_url = urlresolvers.reverse('admin:mediaman_document_change', args=(doc.id,))
            return '<a href="%s">View document record</a>' % (admin_url,)
        except:
            return ''
    view_document.allow_tags = True
    admin_doc_link.allow_tags = True
    verbose_name_plural = 'Related documents'

from django.contrib.admin import SimpleListFilter


class HierarchyListFilter(SimpleListFilter):
    """
    An admin list filter for hierarchical data

    Used for the geo-locations. Is not directly usable, must be overridden
    with appropriate class fields set.

    Designed to be used in order of the hierarchy. Will set a flag and stop
    processing children if a higher level filter is set. So checks the children/parents
    for validity.
    """
    def __init__(self, request, *args):
        super(HierarchyListFilter, self).__init__(
            request, *args)

        if self.is_invalid_parent(self.get_parent(request)):
            request.stop_processing_hierarchy_filter = True

    def is_invalid_parent(self, parent):
        current = None

        val = self.value()
        if val:
            current = self.model.objects.get(id=val)
        return current and current.parent != parent

    def get_parent(self, request):
        if hasattr(self, '_parent'):
            return self._parent
        parent_id = request.GET.get(self.parent_parameter_name)
        parent_field = self.model._meta.get_field_by_name('parent')[0]
        parent_type = parent_field.rel.to
        self._parent = parent_type.objects.filter(id=parent_id)[0] if parent_id else None
        return self._parent

    def lookups(self, request, model_admin):
        if hasattr(request, 'stop_processing_hierarchy_filter'):
            return []
        parent = self.get_parent(request)
        options = self.model.objects.filter(parent=parent)
        return [(str(val.id), val.name) for val in options]

    def queryset(self, request, queryset):
        print 'queryset(): %s' % self.title
        if self.value() and not hasattr(request, 'stop_processing_hierarchy_filter'):
            args = {self.parameter_name: self.value()}
            return queryset.filter(**args)
        else:
            return queryset


class CountryListFilter(HierarchyListFilter):
    title = 'country'
    parameter_name = 'country_id'
    parent_parameter_name = 'global_region__id__exact'
    model = Country


class StateProvinceListFilter(HierarchyListFilter):
    title = 'state/province'
    parameter_name = 'state_province_id'
    parent_parameter_name = 'country_id'
    model = StateProvince


class RegionDistrictListFilter(HierarchyListFilter):
    title = 'region/district'
    parameter_name = 'region_district_id'
    parent_parameter_name = 'state_province_id'
    model = RegionDistrict


class LocalityListFilter(HierarchyListFilter):
    title = 'locality'
    parameter_name = 'country_id'
    parent_parameter_name = 'region_district_id'
    model = Locality


class MOAdmin(UndeleteableModelAdmin):
    list_display = ('registration_number',
                    'description', 'comment', 'public', 'is_public_comment')
    readonly_fields = ('place', 'cultural_bloc', 'functional_category',
        'donor_2', 'collector_2', 'old_registration_number',)

    list_filter = ('artefact_type', 'category',
                    'access_status', 'loan_status',
                    'collector', 'donor', 'record_status',
                    'global_region', CountryListFilter, StateProvinceListFilter,
                    RegionDistrictListFilter, LocalityListFilter, 'is_public_comment',
                    'public', 'maker', 'acquisition_method')

    search_fields = ['registration_number', 'description', 'comment',
                     'donor__name', 'collector__name', 'maker__name',
                     'global_region__name', 'country__name', 'state_province__name',
                     'region_district__name', 'locality__name']

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
    fieldsets = (
        (None, {
            'fields': ('registration_number', 'old_registration_number',
                       'other_number', 'functional_category', 'category',
                       'artefact_type')
        }),
        ('Registration', {
            'fields': ('registered_by', 'registration_date')
        }),
        ('Old place information', {
            'fields': ('cultural_bloc', 'place',)
        }),
        ('Geo-location', {
            'classes': ('collapse',),
            'fields': ('global_region', 'country', 'state_province',
                'region_district', 'locality')
        }),
        ('Status', {
            'classes': ('collapse',),
            'fields': ('loan_status', 'access_status', 'record_status',)
        }),
        ('Storage location', {
            'classes': ('collapse',),
            'fields': ('storage_section', 'storage_unit',
                'storage_bay', 'storage_shelf_box_drawer')
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
            'fields': ('description', 'comment', 'is_public_comment',
                'private_comment', 'significance')
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
            'fields': (('longitude', 'latitude'),)
        }),
        ('Dimensions', {
            'classes': ('collapse',),
            'fields': (('length', 'width', 'height'),
                ('depth', 'circumference'))
        }),
    )

    #### SETUP ADMIN ACTIONS #####
    actions = [add_to_collection, generate_xls, 'make_comment_public',
        'make_comment_private', 'make_record_public', 'make_record_private',
        'move_comment_to_reg_info']

    def make_comment_public(self, request, queryset):
        queryset.update(is_public_comment=True)
    make_comment_public.short_description = "Make research notes public"

    def make_comment_private(self, request, queryset):
        queryset.update(is_public_comment=False)
    make_comment_private.short_description = "Make research notes private"

    def make_record_public(self, request, queryset):
        queryset.update(public=True, is_public_comment=True)
    make_record_public.short_description = "Make entire record public"

    def make_record_private(self, request, queryset):
        queryset.update(public=False, is_public_comment=False)
    make_record_private.short_description = "Make entire record private"

    def move_comment_to_reg_info(self, request, queryset):
        for mo in queryset:
            mo.reg_info = mo.reg_info + '\n\n' + mo.comment
            mo.comment = ''
            mo.save()
    move_comment_to_reg_info.short_description = "Move research notes field to registration notes"

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

    def get_actions(self, request):
        """
        Allow selecting multiple items when change-list is opened as a popup
        """
        from django.contrib.admin.views.main import IS_POPUP_VAR
        if IS_POPUP_VAR in request.GET:
            actions = []
            actions.extend(self.get_action(add_to_opener))
            return SortedDict([
                ('add_to_opener', (add_to_opener, 'add_to_opener', 'Select items'))
            ])
        else:
            return super(MOAdmin, self).get_actions(request)

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', '/static/')
        css = {'all': (static_url + 'museumobject-admin-detail.css',)}


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

