from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from models import MuseumObject, Category
from location.models import Place
from django.db.models import Count
from utils.utils import do_paging
from haystack.views import basic_search
from haystack.forms import SearchForm
from django.shortcuts import redirect
from uqam.utils.utils import url_with_querystring

import string


def home_page(request):
    objects = MuseumObject.objects.exclude(
            artefactrepresentation__isnull=True)
    objects = do_paging(request, objects)

    return render(request, 'index.html',
            {'objects': objects})


def item_detail(request, reg_num):
    mo = get_object_or_404(MuseumObject, registration_number=reg_num)

    images = mo.artefactrepresentation_set.filter(public=True)

    context = {'museumobject': mo, 'images': images}
    search_context = _current_search_results(request, reg_num)
    context.update(search_context)

    return render(request, 'cat/museumobject_detail.html', context)


def _current_search_results(request, reg_num):
    context = {}
    index = request.GET.get('search_result', None)

    if index is not None:
        index = int(index)

        results = request.session.get('search_results', [])
        results_per_page = request.session.get('search_results_per_page')

        context['search_index'] = index
        context['search_results'] = results
        search_query = request.session['search_query']
        page_num = (index / results_per_page) + 1
        search_query.update({'page': page_num})
        search_query.update({'selected_facets': request.session['search_facets']})
        search_url = url_with_querystring(
            reverse('haystack_search'), **search_query)
        context['search_url'] = search_url
        try:
            context['search_next_obj'] = results[index + 1].object
        except:
            pass
        try:
            context['search_prev_obj'] = results[index - 1].object
        except:
            pass
    return context


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


def categories_browse(request):
    """
    Main browse page for categories
    """
    categories = Category.objects.filter(parent=None).exclude(icon_path="")
    equipment = Category.objects.filter(parent__name='Equipment')
    return render(request, 'cat/category_browse.html', {
        'categories': categories,
        'equipment': equipment})


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

    return render(request, "cat/category_list.html", {
            "category": parent,
            "categories": cat_list,
            "objects": objects,
            "breadcrumbs": breadcrumbs[0:-1]})


def search(request):
    '''
    The public search interface.

    Also provides a shortcut of just typing in an object id
    '''
    form = SearchForm(request.GET)
    try:
        if form.is_valid():
            id = int(form.cleaned_data['q'])
            mo = MuseumObject.objects.get(registration_number=id)
            return redirect(mo)
    except:
        pass
    return basic_search(request)


from django.views.generic import ListView


class PeopleListView(ListView):
    template_name = "parties/person_list.html"
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
