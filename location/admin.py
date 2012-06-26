#from django.contrib import admin
from models import Place, Region
from models import GlobalRegion, Country, StateProvince, RegionDistrict, Locality
from tasks import GeocodePlace
from common.adminactions import merge_selected
from django.contrib.gis import admin


class GlobalRegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
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


class PlaceAdmin(admin.OSMGeoAdmin):
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

