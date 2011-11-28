from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import MuseumObject, Place, Category
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.xmlutils import SimplerXMLGenerator


def home_page(request):
    objects = MuseumObject.objects.exclude(artefactrepresentation__isnull=True)
    objects = _do_paging(request, objects)

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
    place_objects = place.museumobject_set.all()

    objects = _do_paging(request, place_objects)

    return render(request, "cat/place_detail.html",
            {'place': place, 'objects': objects})

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
    objects = _do_paging(request, objects)

    return render(request, "cat/category_list.html", 
            {"categories": cat_list,
             "objects": objects,
             "breadcrumbs": breadcrumbs})

def _do_paging(request, queryset):
    paginator = Paginator(queryset, 25)

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
    return objects

def place_kml(request, encoding='utf-8', mimetype='text/plain'):
    """
    Write out all the knows places to KML
    """
    mimetype = "application/vnd.google-earth.kml+xml"
    places = Place.objects.exclude(latitude=None)

    response = HttpResponse(mimetype=mimetype)
    handler = SimplerXMLGenerator(response, encoding)

    handler.startDocument()
    handler.startElement(u"kml", {u"xmlns": u"http://www.opengis.net/kml/2.2"})
    handler.startElement(u"Document", {})

    for place in places:
        handler.startElement(u"Placemark", {})
        handler.addQuickElement(u"name", place.name)
        handler.addQuickElement(u"description", 
                '<a href="%s">%s</a>' % (place.get_absolute_url(), place.__unicode__()))
        handler.startElement(u"Point", {})
        handler.addQuickElement(u"coordinates", place.get_kml_coordinates())
        handler.endElement(u"Point")
        handler.endElement(u"Placemark")

    handler.endElement(u"Document")
    handler.endElement(u"kml")

    return response


