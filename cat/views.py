from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import MuseumObject, Place, Category, Region, Person
from django.db.models import Count
from django.utils.xmlutils import SimplerXMLGenerator
from utils.utils import do_paging


def home_page(request):
    objects = MuseumObject.objects.exclude(artefactrepresentation__isnull=True)
    objects = do_paging(request, objects)

    return render(request, 'index.html',
            {'objects': objects})

def detail(request, artefact_id):
    a = get_object_or_404(MuseumObject, pk=artefact_id)
    return render(request, 'detail.html', {'artefact': a})

def all_countries(request):
    countries = Place.objects.values('country')
    countries = countries.distinct().annotate(count=Count('museumobject'))

    return render(request, 'cat/country_list.html',
            {'countries': countries})

def all_regions(request):
    regions = Place.objects.values('region')
    regions = regions.distinct().annotate(count=Count('museumobject'))
    return render(request, 'cat/region_list.html',
            {'regions': regions})

def regions(request, country):
    regions = Place.objects.filter(country=country).values('region').distinct().annotate(count=Count('museumobject'))
    return render(request, 'cat/region_list.html',
            {'regions': regions})
    
def place_detail(request, place_id):
    """
    Lookup a ``Place`` based on its id. Pagination its objects.
    """
    place = get_object_or_404(Place, pk=place_id)
    try:
        region = Region.objects.get(name=place.region)
    except:
        region = None
    place_objects = place.museumobject_set.all()

    objects = do_paging(request, place_objects)

    return render(request, "cat/place_detail.html",
            {'place': place, 'objects': objects,
             'region': region})

def categories_list(request, full_slug=None):
    """
    Hierarchical browsing of categories

    Based on http://djangosnippets.org/snippets/362/
    """
    parent = None
    breadcrumbs = []
    if full_slug:
        slugs = full_slug.split('/')
        for slug in slugs:
            parent = get_object_or_404(Category, parent=parent, slug__exact=slug)
            breadcrumbs.append(parent)

    cat_list = Category.objects.filter(parent=parent)

    objects = MuseumObject.objects.filter(category=parent)
    objects = do_paging(request, objects)

    return render(request, "cat/category_list.html", 
            {"categories": cat_list,
             "objects": objects,
             "breadcrumbs": breadcrumbs})


def place_kml(request, encoding='utf-8', mimetype='text/plain'):
    """
    Write out all the knows places to KML
    """
#    mimetype = "application/vnd.google-earth.kml+xml"
#    mimetype = "text/html"
    places = Place.objects.exclude(latitude=None).annotate(Count('museumobject'))

    response = HttpResponse(mimetype=mimetype)
    handler = SimplerXMLGenerator(response, encoding)

    handler.startDocument()
    handler.startElement(u"kml", {u"xmlns": u"http://www.opengis.net/kml/2.2"})
    handler.startElement(u"Document", {})

    for place in places:
        place_url = request.build_absolute_uri(place.get_absolute_url())
        handler.startElement(u"Placemark", {})
        handler.addQuickElement(u"name", 
                "%s (%s)" % (place.name, place.museumobject__count))
        handler.addQuickElement(u"description", 
                '<a href="%s">%s</a>' % (place_url, place.__unicode__()))
        handler.startElement(u"Point", {})
        handler.addQuickElement(u"coordinates", place.get_kml_coordinates())
        handler.endElement(u"Point")
        handler.endElement(u"Placemark")

    handler.endElement(u"Document")
    handler.endElement(u"kml")

    return response

from django.core.urlresolvers import reverse
def place_map(request):
    kml_url = request.build_absolute_uri(reverse('place_kml'))
    return render(request, "cat/map.html",
            {"kml_url": kml_url})

def person_list(request):
#    collectors = Person.objects.annotate(Count('collected_objects'))
#    donators = Person.objects.annotate(Count('donated_objects'))
    person_list = Person.objects.annotate(Count('donated_objects')).annotate(Count('collected_objects'))
    #.annotate(Count('collected_objects'))
    return render(request, "cat/person_list.html",
            {"person_list": person_list})
#            {"collectors": collectors,
#             "donators": donators})
