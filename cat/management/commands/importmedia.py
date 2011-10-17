from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from mediaman.models import ArtefactRepresentation, Document
from cat.models import MuseumObject
import os
import re
from os.path import join

def process_path(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            processfile(root, f)

def processfile(root, name):
    match = re.match('(\d+).*jpg$', name)
    if match is None:
        return

    id = match.groups()[0]
    print('ID: %r, file: %r' % (id, join(root, name)))
    add_rep(id, root, name)


def add_rep(id, root, name):
    f = open(join(root,name))
    ar = ArtefactRepresentation()
    ar.name = name
    ar.image = File(f)
    ar.artefact = MuseumObject.objects.get(id=int(id))
    ar.save()
def add_doc(id, name):
    f = open(name)
    doc = Document()
    doc.name = name
    




class Command(BaseCommand):
    help = "Import a dir full of media into the catalogue"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Need one argument for media dir")

        dir, = args

        process_path(dir)
