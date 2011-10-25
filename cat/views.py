# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import MuseumObject, Place
from django.db.models import Count

def index(request):
    return HttpResponse("Hello, world. You're at the catalogue index.")


def detail(request, artefact_id):
    a = get_object_or_404(MuseumObject, pk=artefact_id)
#    try:
#        a = MuseumObject.objects.get(pk=artefact_id)
#    except MuseumObject.DoesNotExist:
#        raise Http404
    return render_to_response('detail.html', {'artefact': a})

def all_countries(request):
    countries = Place.objects.values('country').distinct().annotate(count=Count('museumobject'))

#    countries = Place.objects.values('country').distinct()
    return render_to_response('../templates/cat/country_list.html', {'countries': countries})

def all_regions(request):
    #regions = Place.objects.values('region').distinct()
    regions = Place.objects.values('region').distinct().annotate(count=Count('museumobject'))
    return render_to_response('../templates/cat/region_list.html', {'regions': regions})

def regions(request, country):
    regions = Place.objects.filter(country=country).values('region').distinct().annotate(count=Count('museumobject'))
    return render_to_response('../templates/cat/region_list.html', {'regions': regions})
    
