from django.http import HttpResponseRedirect, HttpResponse
from django.forms import ModelForm
from django import forms
from subcollections.models import Collection
from cat.models import MuseumObject
from utils.utils import do_paging
from django.shortcuts import render, get_object_or_404


def collections_home(request):
    collections = Collection.objects.filter(is_public=True)
    return render(request, 'collections/collections_list.html',
            {'collections': collections})


class SearchSelectMultipleWidget(forms.widgets.SelectMultiple):

    def render():
        pass

    def value_from_datadict():
        pass


class CollectionsForm(ModelForm):
    items = forms.CharField(max_length=100)
    #, widget=SearchSelectMultipleWidget)

    class Meta:
        model = Collection


def collection_edit(request, collection_id):
    if request.method == 'POST':
        form = CollectionsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/collection/')
    else:
        collection = get_object_or_404(Collection, pk=collection_id)
        form = CollectionsForm(instance=collection)
    return render(request, 'collections/collection_edit.html',
            {'collection': collection, 'form': form})


def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id, is_public=True)
    collection_objects = collection.items.all()

    objects = do_paging(request, collection_objects)

    return render(request, 'collections/collection_detail.html',
            {'collection': collection, 'objects': objects})


def collection_add(request):
    """
    Add a group of MuseumObjects to a Collection

    If a Collection is selected, do the modification, if not prompt
    the user to select a Collection.
    """
    ids = []
    if 'ids' in request.GET:
        ids = request.GET.get('ids').split(',')
    if 'selected_collection' in request.POST:
        collection = Collection.objects.get(id=request.POST['selected_collection'])
        selected_objects = MuseumObject.objects.filter(pk__in=ids)
        collection.items.add(*selected_objects)
#        modeladmin.message_user(request, "All %s objects were added to collection: %s." % (selected_objects.count(), collection.title))
        return HttpResponseRedirect("/admin/cat/museumobject/")

    collections = Collection.objects.all()
    return render(request, 'add_to_collection.html',
                {'collections': collections, 'ids': ids})


def atom_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    mimetype = 'application/xml'

    atom = collection.as_atom()
    response = HttpResponse(atom, mimetype=mimetype)
    return response


from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.feedgenerator import rfc3339_date
from utils.utils import get_site_url
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
import StringIO


def atom_feed(request, encoding='utf-8', mimetype='application/atom+xml'):
    feed_attrs = {u"xmlns": u"http://www.w3.org/2005/Atom"}
    collections = Collection.objects.filter(is_public=True)
    site = Site.objects.get(id=1)

    updated = collections.order_by('-updated')[0].updated
    feed_id = get_site_url(site, reverse('atom_feed'))

    output = StringIO.StringIO()
    handler = SimplerXMLGenerator(output, encoding)
    handler.startDocument()
    handler.startElement(u"feed", feed_attrs)

    # Required Attributes
    handler.addQuickElement(u"id", feed_id)
    handler.addQuickElement(u"title", u"UQ Anthropology Museum Sub-collections")
    handler.addQuickElement(u"updated", rfc3339_date(updated).decode('utf-8'))

    # Optional
    handler.addQuickElement(u"link", attrs={
        u'rel': u'alternate',
        u'href': reverse('collections_home'),
        u'type': u'html'
        })

    for collection in collections:
        entry_id = get_site_url(site, collection.get_absolute_url())
        entry_updated = rfc3339_date(collection.updated).decode('utf-8')

        handler.startElement(u"entry", {})
        handler.addQuickElement(u"id", entry_id)
        handler.addQuickElement(u"title", collection.title)
        handler.addQuickElement(u'updated', entry_updated)
        handler.addQuickElement(u'content', attrs={
            u'src': collection.get_atom_url(),
            u'type': u'application/atom+xml'
            })

        handler.endElement(u'entry')

    handler.endElement(u'feed')

    atom = output.getvalue()
    response = HttpResponse(atom, mimetype=mimetype)
    return response

