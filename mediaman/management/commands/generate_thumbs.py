from django.core.management.base import BaseCommand
import easy_thumbnails
from mediaman.models import ArtefactRepresentation
import os


class Command(BaseCommand):
    help = "Generate thumbnails for Artefact Representations"

    def handle(self, *args, **options):
        unbuffered = os.fdopen(self.stdout.fileno(), 'w', 0)
        self.stdout = unbuffered

        ars = ArtefactRepresentation.objects.all()
        self.stdout.write("Found %s images\n" % ars.count())

        for ar in ars:
            # self.stdout.write(str(ar.image) + "\n")
            if ar.image.storage.exists(ar.image):
                easy_thumbnails.files.generate_all_aliases(
                    ar.image, include_global=True)
                self.stdout.write('.')
            else:
                self.stdout.write('n')

        self.stdout.write("\nProcessed all images\n")
