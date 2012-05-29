from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from datetime import datetime
from mediaman.models import ArtefactRepresentation, Document
from cat.models import MuseumObject
from parties.models import Person
import re


def bulk_upload(request):
    form = UploadFileForm()
    return render(request, 'mediaman/upload_form.html',
            {'form': form, 'title': 'Bulk upload'})

UPLOAD_TYPE_CHOICES = (
    ('NO', ''),
    ('II', 'Item Images'),
    ('OH', 'Object Histories'),
    ('SF', 'Source Files'),
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
            elif uploadtype == 'OH':
                handle_object_history(form.cleaned_data, uploadedfile, request.user)
            elif uploadtype == 'SF':
                handle_donor_file(form.cleaned_data, uploadedfile, request.user)
            else:
                return HttpResponse('ERROR: Please select the type of files')
        else:
            return HttpResponse('ERROR: %s' % form.errors)
    else:
        return HttpResponse('ERROR: Only POST requests allowed')

    return HttpResponse('SUCCESS')


def handle_item_image(formdata, ufile, user):
    reg_num = name_to_id(ufile.name, formdata['pathinfo0'])[0]

    ar = set_mediafile_attrs(ArtefactRepresentation(), ufile, formdata, user)
    ar.position = 0
    ar.image = ufile
    ar.artefact = MuseumObject.objects.get(registration_number=reg_num)
    ar.save()


def handle_object_history(formdata, ufile, user):
    reg_nums = name_to_id(ufile.name, formdata['pathinfo0'])
    mo = MuseumObject.objects.filter(registration_number__in=reg_nums)

    doc = make_document(ufile, formdata, user)
    doc.museumobject_set.add(*mo)


def handle_donor_file(formdata, ufile, user):
    person_id = name_to_id(ufile.name, formdata['pathinfo0'])[0]
    person = Person.objects.get(pk=person_id)

    doc = make_document(ufile, formdata, user)
    doc.related_people.add(person)


def make_document(ufile, formdata, user):
    doc = Document()
    doc = set_mediafile_attrs(doc, ufile, formdata, user)
    doc.document = ufile
    doc.save()
    return doc


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


class ParseError(Exception):
    """Unable to parse Id from path/filename"""
    pass


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

    if match:
        return [int(match.group(1))]

    # try using the filepath
    if path is not None:
        # match number range
        match = re.match(r'.*?[/\\].*?(\d+) ?- ?(\d+)', path)

        if match:
            min, max = [int(i) for i in match.groups()]
            return range(min, max + 1)
        else:
            match = re.match(r'.*?[/\\].*?(\d+)', path)

            if match:
                return [int(match.group(1))]

    raise ParseError
