#from django.contrib import admin
from models import Place, Region
from models import GlobalRegion, Country, StateProvince, RegionDistrict, Locality
from tasks import GeocodePlace
from common.adminactions import merge_selected
from django.contrib.gis import admin
from django import forms
from smart_selects.form_fields import ChainedModelChoiceField

admin.site.register(GlobalRegion)
admin.site.register(Country)


class StateProvinceAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StateProvinceAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk is not None:
            initial = {}
            initial['global_region'] = self.instance.parent.parent.pk
            self.initial.update(initial)

    global_region = forms.ModelChoiceField(
        queryset=GlobalRegion.objects.all(), required=False)
    parent = ChainedModelChoiceField(
        'location', 'Country', 'global_region', 'parent', False, False, label='Country')

    class Meta:
        model = Country

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


class GlobalRegionListFilter(SimpleListFilter):
    title = _('global region')
    parameter_name = 'global_region'

    def lookups(self, request, model_admin):
        return [(gr.id, gr.name) for gr in GlobalRegion.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__parent_id=self.value())
        else:
            return queryset


class StateProvinceListFilter(SimpleListFilter):
    title = 'state/province'
    parameter_name = 'state_province'

    def lookups(self, request, model_admin):
        gr_id = request.GET.get('global_region', None)
        return [(sp.id, sp.name) for sp in StateProvince.objects.filter(parent__id=gr_id)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__id=self.value())
        else:
            return queryset


class CountryListFilter(SimpleListFilter):
    title = 'country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        gr_id = request.GET.get('global_region', None)
        return [(c.id, c.name) for c in Country.objects.filter(parent__id=gr_id)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__id=self.value())
        else:
            return queryset


class StateProvinceAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'description', 'gn_name',
        'gn_id', 'global_region', 'parent')
    form = StateProvinceAdminForm
    list_filter = (GlobalRegionListFilter, CountryListFilter)

    def global_region(self, obj):
        return obj.parent.parent.name

    def country(self, obj):
        return obj.parent.name

    def state_province(self, obj):
        return obj.name
    list_display = ('global_region', 'country', 'state_province')


admin.site.register(StateProvince, StateProvinceAdmin)
admin.site.register(RegionDistrict)
admin.site.register(Locality)


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

