from django.shortcuts import render


def bulk_upload(request):
    return render(request, 'mediaman/upload_form.html')
