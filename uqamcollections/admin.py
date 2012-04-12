from django.contrib import admin
from uqamcollections.models import Collection, Syndication
from django.contrib.auth.models import User

#from django.db.models import ManyToManyField


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_public', 'is_syndicated', 'updated')
    search_fields = ['title', 'description', 'author']
    raw_id_fields = ('items',)

    readonly_fields = ('author', 'updated', 'created', 'edit_url',
            'last_published', 'date_published', 'last_syndicated')

    autocomplete_lookup_fields = {
        'm2m': ['items'],
        'fk': ['agent'],
    }

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
            obj.save()

#    formfield_overrides = {
#        ManyToManyField: {'widget': RichTextEditorWidget},
#    }


admin.site.register(Collection, CollectionAdmin)


class SyndicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Syndication, SyndicationAdmin)
