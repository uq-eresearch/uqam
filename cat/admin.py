from django.contrib import admin
from models import MuseumObject,FunctionalCategory

class MOAdmin(admin.ModelAdmin):
    list_display = ('registration_number','country','description','comment',)

    list_filter = ('country','functional_category', 'loan_status', 'cultural_bloc',)

    search_fields = ['registration_number', 'description','comment']


admin.site.register(MuseumObject, MOAdmin)


admin.site.register(FunctionalCategory)
