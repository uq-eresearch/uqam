from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from models import MuseumObject, Place, Category, Region
from django.db.models import Count
from django.utils.xmlutils import SimplerXMLGenerator
from utils.utils import do_paging
import string


def home_page(request):
    objects = MuseumObject.objects.exclude(
            artefactrepresentation__isnull=True)
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
    regions = Place.objects.filter(country=country).values('region').\
                    distinct().annotate(count=Count('museumobject'))
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
            parent = get_object_or_404(Category,
                    parent=parent, slug__exact=slug)
            breadcrumbs.append(parent)

    cat_list = Category.objects.filter(parent=parent)

    objects = MuseumObject.objects.filter(category=parent)
    objects = do_paging(request, objects)

    return render(request, "cat/category_list.html",
            {"categories": cat_list,
             "objects": objects,
             "breadcrumbs": breadcrumbs})

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
    return render(request, "cat/map.html",
            {"kml_url": kml_url})


def place_mapcluster(request):
    kml_url = request.build_absolute_uri(reverse('place_kml'))
    return render(request, "cat/mapcluster.html",
            {"kml_url": kml_url})


def place_duplicates(request):
    '''
    Used for finding duplicate places, by Geoname ID
    '''
    places = Place.objects.values(
            'gn_id').order_by().annotate(
                    count=Count('gn_id')).filter(count__gt=1)
    return render(request, "cat/place_dups_list.html",
            {'places': places})


def place_geoname(request, geoname_id):
    places = Place.objects.filter(gn_id=geoname_id)
    return render(request, "cat/place_geoname.html", {'places': places})

from haystack.views import basic_search
from haystack.forms import SearchForm
from django.shortcuts import redirect


def search(request):
    '''
    The public search interface.

    Also provides a shortcut of just typing in an object id
    '''
    form = SearchForm(request.GET)
    try:
        if form.is_valid():
            id = int(form.cleaned_data['q'])
            mo = MuseumObject.objects.get(pk=id)
            return redirect(mo)
    except:
        pass
    return basic_search(request)


from django.views.generic import ListView


class PeopleListView(ListView):
    template_name = "cat/person_list.html"
    counted_obj = "museumobject"
    paginate_by = 25
    view_name = 'maker_list'
    page_title = 'People'

    def get_queryset(self):
        return self.model.objects.filter(
                name__istartswith=self.kwargs['letter']
            ).exclude(**{self.counted_obj: None}
            ).annotate(
                num_objects=Count(self.counted_obj)
            )

    def get_context_data(self, **kwargs):
        context = super(PeopleListView, self).get_context_data(**kwargs)
        first_letters = self.first_letters()

        # turn into a list of tuples, all letters with a boolean for exists
        first_letters = [(a, a in first_letters) for a in string.lowercase]
        context['first_letters'] = first_letters

        context['base_url'] = reverse(self.view_name)
        context['page_title'] = self.page_title
        return context

    def first_letters(self, name='name'):
        """Returns all the first letters of names, in lowercase"""
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT LOWER(SUBSTR({0}, 1, 1)) as character
            FROM {1}
            WHERE {0} <> ''
            ORDER by character""".format(name, self.model._meta.db_table))
        result_list = []
        for row in cursor.fetchall():
            result_list.append(row[0])
        return result_list
