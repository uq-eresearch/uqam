from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django import forms
from uqamcollections.models import Collection
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


from feeds import write_collection_as_atom
def atom_detail(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    
    response = write_collection_as_atom(request, collection)
    return response

