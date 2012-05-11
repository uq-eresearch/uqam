from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms
from mediaman.models import ArtefactRepresentation
from cat.models import MuseumObject
import re


def bulk_upload(request):
    form = UploadFileForm()
    return render(request, 'mediaman/upload_form.html',
            {'form': form})

UPLOAD_TYPE_CHOICES = (
    ('II', 'Item Images'),
    ('DOC', 'Item Documents'),
#    ('OH', 'Object Histories'),
#    ('CC', 'Catalogue Cards'),
)


class UploadFileForm(forms.Form):
    File0 = forms.FileField()
    mimetype0 = forms.CharField(max_length=60)
    filemodificationdate0 = forms.CharField(max_length=20)
    pathinfo0 = forms.CharField(max_length=255)
    relpathinfo0 = forms.CharField(max_length=255, required=False)
    md5sum0 = forms.CharField(max_length=32)
    uploadtype = forms.ChoiceField(choices=UPLOAD_TYPE_CHOICES)


class ArtForm(forms.ModelForm):
    class Meta:
        model = ArtefactRepresentation


def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


#@csrf_exempt
def handle_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploadtype = form.cleaned_data['uploadtype']
            uploadedfile = form.files['File0']
            if uploadtype == 'II':
                handle_item_image(form, uploadedfile, request.user)
            elif uploadtype == 'DOC':
                handle_document(form, uploadedfile, request.user)

    return render(request, 'mediaman/success_page.html')


def handle_item_image(form, ufile, user):
    item_id = name_to_id(ufile.name)
    cd = form.cleaned_data

    ar = ArtefactRepresentation()
    ar.name = ufile.name
    ar.original_filename = ufile.name
    ar.original_path = cd['pathinfo0']
    #TODO: Uncomment when fixed date format with custom
    # jupload uploadpolicy: http://jupload.sourceforge.net/apidocs/wjhk/jupload2/policies/package-summary.html
    #ar.original_filedate = cd['filemodificationdate0']
    ar.md5sum = cd['md5sum0']
    ar.mime_type = cd['mimetype0']
    ar.user = user
    ar.image = ufile
    ar.filesize = ufile.size
    ar.position = 0
    ar.artefact = MuseumObject.objects.get(registration_number=item_id)
    ar.save()


def name_to_id(filename, path=None):
    """Calculate item id based on filename"""
    match = re.match(r'(\d+).*$', filename)

    # try using the filepath
    if match is None and path:
        match = re.match(r'.*?[/\\](\d+).*', path)

    if match is None:
        return

    id = match.groups()[0]

    return int(id)


def handle_document(form, ufile):
    pass

