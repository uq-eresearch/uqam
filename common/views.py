from haystack.views import FacetedSearchView
from django import forms
from haystack.forms import SearchForm
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.forms import CheckboxInput
from django.utils.safestring import mark_safe


class ExpandableCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])

        choices = self.choices + list(choices)

        selected_choices = [choice for choice in choices if choice[0] in str_values]
        choices = [choice for choice in choices if choice[0] not in str_values]

        for i, (option_value, option_label) in enumerate(selected_choices):
            self.render_checkbox(output, has_id, final_attrs,
                attrs, i, str_values, option_value, name, option_label)

        for i, (option_value, option_label) in enumerate(choices[:5]):
            self.render_checkbox(output, has_id, final_attrs,
                attrs, i, str_values, option_value, name, option_label)

        output.append(u'</ul>')

        if choices[5:]:
            output.append(u'<ul class="extra-options">')

            for i, (option_value, option_label) in enumerate(choices[5:]):
                self.render_checkbox(output, has_id, final_attrs,
                    attrs, i, str_values, option_value, name, option_label)
            output.append(u'</ul>')

            output.append(u'<a href="#" class="display-more">more...</a>')

        return mark_safe(u'\n'.join(output))

    def render_checkbox(self, output, has_id, final_attrs, attrs, i, str_values, option_value, name, option_label):
        # If an ID attribute was given, add a numeric index as a suffix,
        # so that the checkboxes don't all have the same ID attribute.
        if has_id:
            final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
            label_for = u' for="%s"' % final_attrs['id']
        else:
            label_for = ''

        cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
        option_value = force_unicode(option_value)
        rendered_cb = cb.render(name, option_value)
        option_label = conditional_escape(force_unicode(option_label))
        output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))


class UnvalidatedMultipleChoiceField(forms.MultipleChoiceField):
    widget = ExpandableCheckboxSelectMultiple

    def validate(self, value):
        """
        Validates that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])


class CatalogueSearchForm(SearchForm):
    category = UnvalidatedMultipleChoiceField(required=False)
    global_region = UnvalidatedMultipleChoiceField(required=False)
    country = UnvalidatedMultipleChoiceField(required=False)
    item_name = UnvalidatedMultipleChoiceField(required=False)
    person = forms.CharField(required=False)
    has_images = forms.BooleanField(required=False, label="Only return results with an associated image")

    # def __init__(self, *args, **kwargs):
    #     self.item_names = kwargs.pop("item_names", [])

    #     super(CatalogueSearchForm, self).__init__(*args, **kwargs)


class PersistentSearchView(FacetedSearchView):
    __name__ = "PersistentSearchView"

    def extra_context(self):
        """
        Save results to session
        """
        extra = super(PersistentSearchView, self).extra_context()

        if self.form.is_valid():
            self.request.session['search_query'] = self.form.cleaned_data
            self.request.session['search_facets'] = self.form.selected_facets
        if self.results:
            # Access the first result to prevent ZeroDivisionError
            self.results[0]
        self.request.session['search_results'] = self.results
        self.request.session['search_results_per_page'] = self.results_per_page
        return extra

from django.core.paginator import Paginator, InvalidPage
from django.template import RequestContext
from haystack.query import EmptySearchQuerySet
from django.conf import settings
from django.shortcuts import render
from django.http import Http404

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


def catalogue_search(request, template='search/search.html', load_all=True,
    form_class=CatalogueSearchForm, searchqueryset=None, extra_context=None,
    results_per_page=None):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.

    Useful as an example of for basing heavily custom views off of.

    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.

    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = EmptySearchQuerySet()
    results_per_page = results_per_page or RESULTS_PER_PAGE

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    results = results.facet('categories').facet('country').facet('has_images').facet('global_region').facet('item_name')

    facets = results.facet_counts()

    if form.is_valid():
        results = filter_with_facet(form, results, facets, 'item_name', 'item_name')
        results = filter_with_facet(form, results, facets, 'category', 'categories')
        results = filter_with_facet(form, results, facets, 'global_region', 'global_region')
        results = filter_with_facet(form, results, facets, 'country', 'country')

        if form.cleaned_data['person']:
            results = results.narrow(u'people:"%s"' % form.cleaned_data['person'])

        if form.cleaned_data['has_images'] == True:
            results = results.narrow(u'has_images_exact:true')

    paginator = Paginator(results, results_per_page)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
        'facets': facets,
    }

    # Store query for paging through results on item detail page
    if form.is_valid():
        request.session['search_query'] = form.cleaned_data
    # Access the first result to prevent ZeroDivisionError
    if results:
        results[0]
    request.session['search_results'] = results
    request.session['search_results_per_page'] = results_per_page

    if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render(request, template, context)


def filter_with_facet(form, results, facets, form_field_name, facet_name):
    if form.cleaned_data[form_field_name]:
        ins = None
        for itn in form.cleaned_data[form_field_name]:
            if ins:
                ins += u' OR '
            else:
                ins = u''
            ins += u'"%s"' % results.query.clean(itn)

        results = results.narrow(facet_name + u'_exact:%s' % ins)

    if facets['fields'][facet_name]:
        form.fields[form_field_name].choices = [
            (facet[0], "%s (%s)" % (facet[0], facet[1]))
            for facet in facets['fields'][facet_name]]

    return results
