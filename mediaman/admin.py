from django.contrib import admin
from models import Document, ArtefactRepresentation
from cat.models import MuseumObject
from parties.models import Person
from django.core import urlresolvers

mediafile_readonly = ('md5sum', 'file_size', 'uploaded_by', 'mime_type',
        'original_filename', 'original_path', 'original_filedate',
        'name')


class MOInline(admin.TabularInline):
    model = MuseumObject.related_documents.through
    fields = ('museumobject', 'item_link',)
    readonly_fields = ('item_link',)
    def item_link(self, obj):
        if obj.museumobject:
            mo = obj.museumobject
            admin_url = urlresolvers.reverse('admin:cat_museumobject_change', args=(mo.id,))
            return '<a href="%s">%s</a>' % (admin_url, mo.__unicode__())
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
            p = obj.person
            admin_url = urlresolvers.reverse('admin:parties_person_change', args=(p.id,))
            return '<a href="%s">%s</a>' % (admin_url, p.display_name)
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
    list_display = ('__unicode__', 'related_items', 'upload_date', 'public')

admin.site.register(Document, DocumentAdmin)


class ArtefactRepresentationAdmin(MediaFileAdmin):
    readonly_fields = ('image', 'artefact', 'position') + mediafile_readonly + ('thumbnail',)
    fields = readonly_fields
    list_display = ('__unicode__', 'artefact', 'upload_date')

    def thumbnail(self, obj):
        try:
            thumb_opts = {'size': (64, 64), 'watermark': ''}
            thumb = obj.image.get_thumbnail(thumb_opts)
            return '<a href="%s"><img src="%s"></a>' % (obj.image.url, thumb.url)
        except:
            return 'Error generating thumbnail'
    thumbnail.allow_tags = True



admin.site.register(ArtefactRepresentation, ArtefactRepresentationAdmin)
