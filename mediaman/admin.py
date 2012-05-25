from django.contrib import admin
from models import Document, ArtefactRepresentation
from cat.models import MuseumObject
from parties.models import Person

mediafile_readonly = ('md5sum', 'filesize', 'uploaded_by', 'mime_type',
        'original_filename', 'original_path', 'original_filedate',
        'name')


class MOInline(admin.TabularInline):
    model = MuseumObject.related_documents.through
    fields = ('museumobject', 'item_link',)
    readonly_fields = ('item_link',)
    def item_link(self, obj):
        if obj.museumobject:
            return '<a href="%s">%s</a>' % (obj.museumobject.get_absolute_url(), obj.museumobject.__unicode__())
        else:
            return ''
    item_link.allow_tags = True
    verbose_name_plural = 'Related museum items'

    raw_id_fields = ('museumobject',)


class PersonInline(admin.TabularInline):
    model = Person.related_documents.through
    fields = ('person', 'person_link',)
    readonly_fields = ('person_link',)
    def person_link(self, obj):
        if obj.person:
            return '<a href="%s">%s</a>' % (obj.person.get_absolute_url(), obj.person.display_name)
        else:
            return ''
    person_link.allow_tags = True
    verbose_name_plural = 'Related people'
    raw_id_fields = ('person',)


class MediaFileAdmin(admin.ModelAdmin):
    ordering = ('-upload_date',)

    def has_add_permission(self, request):
        '''Always deny adding in admin

        Files should always be uploaded through the bulk upload tool
        '''
        return False


class DocumentAdmin(MediaFileAdmin):
    readonly_fields = ('document', ) + mediafile_readonly + ('document_link',)
    fields = ('document',) + mediafile_readonly + ('document_text', 'public', 'document_link',)
    def document_link(self, obj):
        doc = obj.document
        return '<a href="%s">%s</a>' % (doc.url, doc.name)
    document_link.allow_tags = True
    inlines = [MOInline, PersonInline]

    def related_items(self, obj):
        return ", ".join([str(m.registration_number) for m in obj.museumobject_set.all()])

    def related_people(self, obj):
        return " ".join([str(m) for m in obj.museumobject_set.all()])
    list_display = ('__unicode__', 'related_items', 'upload_date')

admin.site.register(Document, DocumentAdmin)


class ArtefactRepresentationAdmin(MediaFileAdmin):
    readonly_fields = ('image', 'artefact', 'position') + mediafile_readonly

    list_display = ('__unicode__', 'artefact', 'upload_date')


admin.site.register(ArtefactRepresentation, ArtefactRepresentationAdmin)
