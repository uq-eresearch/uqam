from haystack.views import SearchView


class PersistentSearchView(SearchView):
    __name__ = "PersistentSearchView"

    def extra_context(self):
        """
        Save results to session
        """
        extra = super(PersistentSearchView, self).extra_context()
        if self.form.cleaned_data and self.results:
#            self.request.session['search_query'] = self.form.cleaned_data
            self.request.session['search_results'] = self.results
        return extra

    def playingaround(self):
        sticks = SearchQuerySet().filter(content='stick')
        ids = [y.id for y in sticks.query.get_results()]

