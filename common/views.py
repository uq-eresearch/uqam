from haystack.views import SearchView
import logging

logger = logging.getLogger(__name__)


class PersistentSearchView(SearchView):
    __name__ = "PersistentSearchView"

    def extra_context(self):
        """
        Save results to session
        """
        extra = super(PersistentSearchView, self).extra_context()

        if self.form.is_valid():
            self.request.session['search_query'] = self.form.cleaned_data
#        import ipdb; ipdb.set_trace()
        if self.results:
            # Access the first result to prevent ZeroDivisionError
            self.results[0]
        self.request.session['search_results'] = self.results
        self.request.session['search_results_per_page'] = self.results_per_page
        return extra

