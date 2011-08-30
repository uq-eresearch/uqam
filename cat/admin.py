from django.contrib import admin
from models import MuseumObject,FunctionalCategory

class MOAdmin(admin.ModelAdmin):
    fields = ('registration_number','country','description','comment')

    list_display = ('registration_number','country','description','comment')

    list_filter = ('country','functional_category')

    search_fields = ['description','comment']


admin.site.register(MuseumObject, MOAdmin)


admin.site.register(FunctionalCategory)
