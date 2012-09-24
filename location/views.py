from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.xmlutils import SimplerXMLGenerator
from models import Place, Region
from models import Locality
from models import GlobalRegion
from utils.utils import do_paging, split_list
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
import json


def place_detail(request, place_id):
    """
    Lookup a ``Place`` based on its id. Pagination its objects.
    """
    place = get_object_or_404(Place, pk=place_id)
    try:
        region = Region.objects.get(name=place.region)
    except:
        region = None
    place_objects = place.museumobject_set.filter(public=True)

    objects = do_paging(request, place_objects)

    return render(request, "location/place_detail.html",
            {'place': place, 'objects': objects,
             'region': region})


def place_json(request, encoding='utf-8', mimetype='text/plain'):
    places = Locality.objects.exclude(
            latitude=None).annotate(Count('museumobject')).values(
            'id', 'name', 'latitude', 'longitude',
            'museumobject__count')
    return HttpResponse(json.dumps(list(places), indent=2))


def place_kml(request, encoding='utf-8', mimetype='text/plain'):
    """
    Write out all the known places to KML
    """
#    mimetype = "application/vnd.google-earth.kml+xml"
#    mimetype = "text/html"
    places = Locality.objects.exclude(
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


def find_location(model_type, id):
    element_type = ContentType.objects.get(app_label='location', model=model_type)
    return element_type.get_object_for_this_type(id=id)


def view_places(request):
    grs = GlobalRegion.objects.exclude(icon_path="").prefetch_related('children')
    d = dict((g.name, g) for g in grs)
    grs = [d['Australia'], d['Pacific'], d['Asia'], d['Europe'], d['Americas'], d['Africa'],
        d['Middle East']]

    kml_url = request.build_absolute_uri(reverse('place_kml'))

    return render(request, 'location/map.html',
        {'global_regions': grs,
         'kml_url': kml_url})


def view_geoloc(request, loctype, id, columns=3):

    geolocation = find_location(loctype, id)

    items = geolocation.museumobject_set.select_related().filter(public=True
        ).prefetch_related('category', 'country', 'global_region'
        ).extra(
            select={'public_images_count': 'select count(*) from mediaman_artefactrepresentation a WHERE a.artefact_id = cat_museumobject.id AND a.public'})

    children = []
    if hasattr(geolocation, 'children'):
        children = geolocation.children.all()

    objects = do_paging(request, items)

    return render(request, 'location/geolocation.html',
        {'geolocation': geolocation,
         'objects': objects,
         'num_children': len(children),
         'children': split_list(children, parts=columns)})

