from django.contrib import admin
from models import MuseumObject,FunctionalCategory,Person, Place
from models import CulturalBloc, MediaRepresentation

class MOAdmin(admin.ModelAdmin):
    list_display = ('registration_number','cultural_bloc','description','comment',)

    list_filter = ('place__country','functional_category__name', 'access_status', 'loan_status', 'cultural_bloc',)

    search_fields = ['registration_number', 'description','comment']


admin.site.register(MuseumObject, MOAdmin)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('country', 'region', 'australian_state', 'name',)
    list_filter = ('country', 'australian_state', 'region',)
admin.site.register(Place, PlaceAdmin)

admin.site.register(FunctionalCategory)
admin.site.register(CulturalBloc)
admin.site.register(MediaRepresentation)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'comments',)
    search_fields = ['name', 'comments',]
admin.site.register(Person, PersonAdmin)
