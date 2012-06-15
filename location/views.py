from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.xmlutils import SimplerXMLGenerator
from models import Place, Region
from models import GlobalRegion
from utils.utils import do_paging
from django.db.models import Count


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

    return render(request, "location/place_detail.html",
            {'place': place, 'objects': objects,
             'region': region})


def place_json(request, encoding='utf-8', mimetype='text/plain'):
    import json
    places = Place.objects.exclude(
            latitude=None).annotate(Count('museumobject')).values(
            'id', 'name', 'latitude', 'longitude', 'country',
            'museumobject__count')
    return HttpResponse(json.dumps(list(places), indent=2))


def place_kml(request, encoding='utf-8', mimetype='text/plain'):
    """
    Write out all the known places to KML
    """
#    mimetype = "application/vnd.google-earth.kml+xml"
#    mimetype = "text/html"
    places = Place.objects.exclude(
            latitude=None).annotate(Count('museumobject'))

    response = HttpResponse(mimetype=mimetype)
    handler = SimplerXMLGenerator(response, encoding)

    handler.startDocument()
    handler.startElement(u"kml",
            {u"xmlns": u"http://www.opengis.net/kml/2.2"})
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


def place_map(request):
    kml_url = request.build_absolute_uri(reverse('place_kml'))
    return render(request, "location/map.html",
            {"kml_url": kml_url})


def place_mapcluster(request):
    kml_url = request.build_absolute_uri(reverse('place_kml'))
    return render(request, "location/mapcluster.html",
            {"kml_url": kml_url})


def place_duplicates(request):
    '''
    Used for finding duplicate places, by Geoname ID
    '''
    places = Place.objects.values(
            'gn_id').order_by().annotate(
                    count=Count('gn_id')).filter(count__gt=1)
    return render(request, "location/place_dups_list.html",
            {'places': places})


def place_geoname(request, geoname_id):
    places = Place.objects.filter(gn_id=geoname_id)
    return render(request, "location/place_geoname.html", {'places': places})


def tree_view(request):
    global_regions = GlobalRegion.objects.all()
    return render(request, "location/tree_view.html",
        {'global_regions': global_regions})
