from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django import forms
from django.template import RequestContext
from uqamcollections.models import Collection
from cat.models import MuseumObject
from django.shortcuts import render_to_response, get_object_or_404

def collections_home(request):
    collections = Collection.objects.all()
    return render_to_response('collections/collections_list.html',
            {'collections': collections},
            context_instance=RequestContext(request))

class SearchSelectMultipleWidget(forms.widgets.SelectMultiple):
    def render():
        pass
    def value_from_datadict():
        pass

class CollectionsForm(ModelForm):
    items = forms.CharField(max_length=100)#, widget=SearchSelectMultipleWidget)
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
    return render_to_response('collections/collection_edit.html',
            {'collection': collection, 'form': form},
            context_instance=RequestContext(request))

def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    return render_to_response('collections/collection_detail.html',
            {'collection': collection},
            context_instance=RequestContext(request))


def collection_add(request):
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
    return render_to_response('add_to_collection.html',{ 'collections': collections, 'ids': ids},
                              context_instance=RequestContext(request))

