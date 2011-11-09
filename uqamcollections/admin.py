from django.contrib import admin
from uqamcollections.models import Collection


class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title','description','agent']
    raw_id_fields = ('items',)


admin.site.register(Collection, CollectionAdmin)
