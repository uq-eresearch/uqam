from django.contrib import admin
from models import Document, ArtefactRepresentation
from cat.models import MuseumObject

mediafile_readonly = ('md5sum', 'filesize', 'uploaded_by', 'mime_type',
        'original_filename', 'original_path', 'original_filedate',
        'name')


class MOInline(admin.TabularInline):
    model = MuseumObject.related_documents.through
    fields = ('document', 'museumobject')
    raw_id_fields = ('document', 'museumobject')


class MediaFileAdmin(admin.ModelAdmin):
    ordering = ('-upload_date',)

    def has_add_permission(self, request):
        '''Always deny adding in admin

        Files should always be uploaded through the bulk upload tool
        '''
        return False


class DocumentAdmin(MediaFileAdmin):
    readonly_fields = ('document', ) + mediafile_readonly
    inlines = [MOInline]

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
