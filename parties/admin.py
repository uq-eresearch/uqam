from django.contrib import admin
from models import Person
from models import Maker
from models import MuseumStaff
from models import Client
from cat.admin import MediaFileInline
from django.core import urlresolvers
from common.adminactions import merge_selected


class DocumentInline(MediaFileInline):
    model = Person.related_documents.through
    fields = ('document_link',)
    readonly_fields = ('document_link',)

    def document_link(self, obj):
        try:
            doc = obj.document.document
            admin_url = urlresolvers.reverse('admin:mediaman_document_change', args=(doc.id,))
            return '<a href="%s">%s</a>' % (admin_url, doc.name)
        except:
            return ''
    document_link.allow_tags = True
    verbose_name_plural = 'Related documents'


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'comments',)
    search_fields = ['name', 'comments']
    fields = ('name', 'display_name', 'comments')
    inlines = [DocumentInline]
    actions = [merge_selected]
admin.site.register(Person, PersonAdmin)


class MakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')
    search_fields = ('name', 'comment')
admin.site.register(Maker, MakerAdmin)


admin.site.register(Client)


class MuseumStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'comments')
    search_fields = ('name', 'comments')
    model = MuseumStaff
admin.site.register(MuseumStaff, MuseumStaffAdmin)
