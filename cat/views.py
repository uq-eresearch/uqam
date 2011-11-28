from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import MuseumObject, Place
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, InvalidPage


def home_page(request):
    objects = MuseumObject.objects.exclude(artefactrepresentation__isnull=True)
    objects = _do_paging(request, objects)

    return render(request, 'index.html',
            {'objects': objects})

def detail(request, artefact_id):
    a = get_object_or_404(MuseumObject, pk=artefact_id)
    return render(request, 'detail.html', {'artefact': a})

def all_countries(request):
    countries = Place.objects.values('country').distinct().annotate(count=Count('museumobject'))

#    countries = Place.objects.values('country').distinct()
    return render(request, 'cat/country_list.html',
            {'countries': countries})

def all_regions(request):
    #regions = Place.objects.values('region').distinct()
    regions = Place.objects.values('region').distinct().annotate(count=Count('museumobject'))
    return render(request, 'cat/region_list.html',
            {'regions': regions})

def regions(request, country):
    regions = Place.objects.filter(country=country).values('region').distinct().annotate(count=Count('museumobject'))
    return render(request, 'cat/region_list.html',
            {'regions': regions})
    
def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    place_objects = place.museumobject_set.all()
    paginator = Paginator(place_objects, 25)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)


    return render(request, "cat/place_detail.html",
            {'place': place, 'objects': objects})
