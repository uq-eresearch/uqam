from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django import forms
from datetime import datetime
from mediaman.models import ArtefactRepresentation, Document
from cat.models import MuseumObject
import re


def bulk_upload(request):
    form = UploadFileForm()
    return render(request, 'mediaman/upload_form.html',
            {'form': form, 'title': 'Bulk upload'})

UPLOAD_TYPE_CHOICES = (
    ('II', 'Item Images'),
    ('DOC', 'Item Documents'),
#    ('OH', 'Object Histories'),
#    ('CC', 'Catalogue Cards'),
)


class UploadFileForm(forms.Form):
    File0 = forms.FileField()
    mimetype0 = forms.CharField(max_length=120)
    filemodificationdate0 = forms.CharField(max_length=20)
    pathinfo0 = forms.CharField(max_length=255)
    relpathinfo0 = forms.CharField(max_length=255, required=False)
    md5sum0 = forms.CharField(max_length=32)
    uploadtype = forms.ChoiceField(choices=UPLOAD_TYPE_CHOICES)


def handle_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploadtype = form.cleaned_data['uploadtype']
            uploadedfile = form.files['File0']
            if uploadtype == 'II':
                handle_item_image(form.cleaned_data, uploadedfile, request.user)
            elif uploadtype == 'DOC':
                handle_document(form.cleaned_data, uploadedfile, request.user)

    return HttpResponse('SUCCESS')


def handle_item_image(formdata, ufile, user):
    reg_num = name_to_id(ufile.name, formdata['pathinfo0'])

    ar = set_mediafile_attrs(ArtefactRepresentation(), ufile, formdata, user)
    ar.position = 0
    ar.image = ufile
    ar.artefact = MuseumObject.objects.get(registration_number=reg_num)
    ar.save()


def handle_document(formdata, ufile, user):
    reg_num = name_to_id(ufile.name, formdata['pathinfo0'])
    mo = MuseumObject.objects.get(registration_number=reg_num)


    doc = Document()
    doc = set_mediafile_attrs(doc, ufile, formdata, user)
    doc.document = ufile
    doc.save()
    doc.museumobject_set.add(mo)


def set_mediafile_attrs(mediafile, ufile, data, user):
    """
    Copy metadata from uploaded file into Model
    """
    mediafile.name = ufile.name
    mediafile.original_filename = ufile.name
    mediafile.filesize = ufile.size
    mediafile.original_path = data['pathinfo0']
    # Date format from jupload is "dd/MM/yyyy HH:mm:ss"
    filedate = datetime.strptime(data['filemodificationdate0'],
        "%d/%m/%Y %H:%M:%S")
    mediafile.original_filedate = filedate
    mediafile.md5sum = data['md5sum0']
    mediafile.mime_type = data['mimetype0']
    mediafile.uploaded_by = user
    return mediafile


def name_to_id(filename, path=None):
    """
    Calculate item id based on filename and path

    12345.jpg = 12345
    1234_2.jpg = 1234

    /home/test/files/12345/cond.tiff = 12345
    S:\\scanned\\1252\\cond.tiff = 1252

    Will also work on a range of ids, returning a list.
    eg: S:\\scanned\\755-762\\test.pdf = [755, 756, ..., 762]

    """
    match = re.match(r'(\d{1,5}).*$', filename)

    # try using the filepath
    if match is None and path:
        match = re.match(r'.*?[/\\]([\d-]+).*', path)

    if match is None:
        return

    id = match.groups()[0]

    if '-' in id: # range of ids
        min, max = [int(i) for i in id.split('-')]
        return range(min, max+1)

    return int(id)


