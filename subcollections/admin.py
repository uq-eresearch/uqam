from django.contrib import admin
from subcollections.models import Collection, Syndication


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
        obj.author = request.user
        obj.save()


admin.site.register(Collection, CollectionAdmin)


class SyndicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Syndication, SyndicationAdmin)
