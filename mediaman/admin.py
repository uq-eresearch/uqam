from django.contrib import admin
from models import Document, ArtefactRepresentation

admin.site.register(Document)


class ArtefactRepresentationAdmin(admin.ModelAdmin):
    raw_id_fields = ('artefact',)
admin.site.register(ArtefactRepresentation, ArtefactRepresentationAdmin)
