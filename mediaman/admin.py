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

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('document', ) + mediafile_readonly
    inlines = [
        MOInline
    ]
admin.site.register(Document, DocumentAdmin)


class ArtefactRepresentationAdmin(admin.ModelAdmin):
    readonly_fields = ('image', 'artefact', 'position' ) + mediafile_readonly


admin.site.register(ArtefactRepresentation, ArtefactRepresentationAdmin)
