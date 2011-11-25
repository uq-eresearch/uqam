from django.contrib import admin
from uqamcollections.models import Collection

#from django.db.models import ManyToManyField


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_public', 'is_syndicated', 'updated')
    search_fields = ['title','description','author']
    raw_id_fields = ('items','author')

    autocomplete_lookup_fields = {
        'm2m': ['items'],
        'fk': ['agent'],
    }



#    formfield_overrides = {
#        ManyToManyField: {'widget': RichTextEditorWidget},
#    }


admin.site.register(Collection, CollectionAdmin)
