#from django.contrib import admin
from models import Place, Region
from tasks import GeocodePlace
from common.adminactions import merge_selected
from django.contrib.gis import admin


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

