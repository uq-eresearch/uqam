#from django.contrib import admin
from models import Place, Region
from models import GlobalRegion, Country, StateProvince, RegionDistrict, Locality
from tasks import GeocodePlace
from common.adminactions import merge_selected
from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from admin_views import jstree, move_element, rename_element
from admin_views import create_element, delete_element


class GlobalRegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

    def get_urls(self):
        urls = super(GlobalRegionAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^jstree$', self.admin_site.admin_view(jstree), name='jstree'),
            url(r'^move_element', self.admin_site.admin_view(move_element), name='move_element'),
            url(r'^rename_element', self.admin_site.admin_view(rename_element), name='rename_element'),
            url(r'^create_element', self.admin_site.admin_view(create_element), name='create_element'),
            url(r'^delete_element', self.admin_site.admin_view(delete_element), name='delete_element'),
        )
        return my_urls + urls
admin.site.register(GlobalRegion, GlobalRegionAdmin)


class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Country, CountryAdmin)


class StateProvinceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    fields = ('name', 'slug', 'description', 'gn_name',
        'gn_id', 'parent')

    def global_region(self, obj):
        return obj.parent.parent.name

    def country(self, obj):
        return obj.parent.name

    def state_province(self, obj):
        return obj.name
    list_display = ('global_region', 'country', 'state_province')
admin.site.register(StateProvince, StateProvinceAdmin)


class RegionDistrictAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(RegionDistrict, RegionDistrictAdmin)


class LocalityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Locality, LocalityAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']
admin.site.register(Region, RegionAdmin)


class PlaceAdmin(admin.ModelAdmin):
    default_zoom = 1
    list_display = ('id', 'country', 'region', 'australian_state',
            'name', 'gn_name')
    list_filter = ('country', 'australian_state', 'region',)

    def geocode_place(modeladmin, request, queryset):
        for place in queryset:
            GeocodePlace.delay(place.id)
    geocode_place.short_description = "Lookup latitude/longitude"

    def geocode_local(modeladmin, request, queryset):
        pass

    actions = [merge_selected, geocode_place]
    search_fields = ['country', 'region', 'australian_state', 'name']
admin.site.register(Place, PlaceAdmin)

