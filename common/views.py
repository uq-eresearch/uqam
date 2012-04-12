from django.shortcuts import render
from cat.models import MuseumObject, ArtefactType, Category
from django import forms
from django.db.models import Q
from django.http import HttpResponse


# Based on code from:
# http://www.slideshare.net/tpherndon/django-search-presentation

class SearchForm(forms.Form):
    """
    Advanced search form for Museum Objects
    """
    keywords = forms.CharField(
        help_text='Keyword search of item comments and description',
        required=False)
    item_type = forms.ModelChoiceField(queryset=ArtefactType.objects.all(),
            required=False)
    region = forms.CharField(help_text='Region item is from', required=False)
    material = forms.CharField(help_text='Material item is made from',
            required=False)
    people = forms.CharField(help_text='Associated people', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
            required=False)
    # maybe dates


def search_home2(request, form_class=SearchForm,
        template_name='common/search_home.html'):
    """
    Advanced search view
    """
    form = None
    if request.method == 'POST':
        #do search
        form = form_class(request.POST)
        if form.is_valid():
            results = search(form.cleaned_data)
            if results:
                return render(template_name, {'form': form, 'items': results})
    else:
        form = form_class()
    return render(request, template_name, {'form': form})


def search(search_data):
    """
    Iterates over all submitted data. For each field, calls
    a method search_'fieldname' on the Searcher.
    """
    q = Q()
    results = None
    searcher = ItemSearch(search_data)

    for key in search_data.iterkeys():
        dispatch = getattr(searcher, 'search_%s' % key)
        q = dispatch(q)

    if q and len(q):
        results = MuseumObject.objects.filter(q).select_related()  # order_by
    else:
        results = []
    return results


class ItemSearch(object):
    def __init__(self, search_data):
        # Include all the form data in self
        self.__dict__.update(search_data)

    def search_keywords(self, q):
        """
        Search should do both title and description, and OR the results
        together, and must iterate over list of keywords
        """
        if self.keywords:
            words = self.keywords.split()
            title_q = Q()
            desc_q = Q()
            for word in words:
                title_q = title_q | Q(title__icontains=word)
                desc_q = desc_q | Q(description__icontains=word)
            keyword_q = title_q | desc_q
            q = q & keyword_q
        return q

    def search_region(self, q):
        return q

    def search_material(self, q):
        return q

    def search_people(self, q):
        return q

    def search_date_added(self, q):
        if self.date_added:
            q = q & Q(date_added__exact=self.date_added)
        return q

    def search_item_type(self, q):
        if self.item_type:
            q = q & Q(artefact_type__icontains=self.artefact_type)
        return q

    def search_category(self, q):
        """
        ManyToMany search
        """
        if self.category:
            if isinstance(self.category, list):
                q = q & Q(category__in=self.category)
            else:
                q = q & Q(category__icontains=self.category)
        return q


