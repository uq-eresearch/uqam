from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from models import MuseumObject, Category, ArtefactType
from uqam.utils.utils import url_with_querystring
from utils.utils import do_paging, split_list


def home_page(request):
    objects = MuseumObject.objects.exclude(
            artefactrepresentation__isnull=True)
    objects = do_paging(request, objects)

    return render(request, 'index.html',
            {'objects': objects})


def item_detail(request, reg_num):
    mo = get_object_or_404(MuseumObject, registration_number=reg_num, public=True)

    images = mo.public_images()

    context = {'museumobject': mo, 'images': images}
    search_context = _current_search_results(request, reg_num)
    context.update(search_context)

    return render(request, 'cat/museumobject_detail.html', context)


def _current_search_results(request, reg_num):
    context = {}
    index = request.GET.get('search_result', None)

    search_query = request.session.get('search_query', {})
    if index is not None and search_query:
        index = int(index) - 1

        results = request.session.get('search_results', [])
        results_per_page = request.session.get('search_results_per_page')

        context['search_result'] = index + 1
        context['search_results'] = results
        page_num = (index / results_per_page) + 1
        search_query.update({'page': page_num})
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


def categories_browse(request):
    """
    Main browse page for categories
    """
    categories = Category.objects.filter(parent=None).exclude(icon_path="")
    equipment = Category.objects.filter(parent__name='Equipment')
    return render(request, 'cat/category_browse.html', {
        'categories': categories,
        'equipment': equipment})


def categories_list(request, full_slug=None, columns=3):
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

    ms = parent.museumobject_set.filter(public=True)
    item_types = ArtefactType.objects.filter(
        id__in=ms.values_list('artefact_type', flat=True).distinct())
    # item_types = parent.suggested_artefact_types.all()

    objects = MuseumObject.objects.filter(category=parent, public=True)
    objects = do_paging(request, objects)

    return render(request, "cat/category_list.html", {
            "category": parent,
            "categories": cat_list,
            "objects": objects,
            "breadcrumbs": breadcrumbs[0:-1],
            "num_item_types": len(item_types),
            "item_types": split_list(item_types, parts=columns)})


def item_type_list(request, category=None, item_name=None):
    category = get_object_or_404(Category, slug__exact=category)
    artefact_type = get_object_or_404(ArtefactType, name=item_name)

    breadcrumbs = []
    if category.parent:
        breadcrumbs.append(category.parent)
    breadcrumbs.append(category)

    objects = MuseumObject.objects.filter(
        category=category, artefact_type=artefact_type, public=True)
    objects = do_paging(request, objects)

    return render(request, "cat/category_list.html", {
            "breadcrumbs": breadcrumbs,
            "category": artefact_type,
            "objects": objects
        })


