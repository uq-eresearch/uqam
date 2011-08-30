from django.contrib import admin
from models import MuseumObject,FunctionalCategory,Person

class MOAdmin(admin.ModelAdmin):
    list_display = ('registration_number','country','description','comment',)

    list_filter = ('country','functional_category', 'loan_status', 'cultural_bloc',)

    search_fields = ['registration_number', 'description','comment']


admin.site.register(MuseumObject, MOAdmin)


admin.site.register(FunctionalCategory)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'comments',)
    search_fields = ['name', 'comments',]
admin.site.register(Person, PersonAdmin)
