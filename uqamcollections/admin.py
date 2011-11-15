from django.contrib import admin
from uqamcollections.models import Collection

from django.db.models import ManyToManyField


class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title','description','agent']
    raw_id_fields = ('items','agent')

    autocomplete_lookup_fields = {
        'm2m': ['items'],
        'fk': ['agent'],
    }



#    formfield_overrides = {
#        ManyToManyField: {'widget': RichTextEditorWidget},
#    }


admin.site.register(Collection, CollectionAdmin)
