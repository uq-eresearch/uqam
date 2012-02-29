from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard


class UQAMDashboard(Dashboard):
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        self.children.append(modules.AppList(
            title=_('Catalogue'),
            column=1,
            collapsible=False,
            exclude=('django.contrib.*', 'djcelery.*', 'reports.*'),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            column=1,
            collapsible=True,
            models=('django.contrib.*', 'djcelergy.*', 'reports.*'),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            column=2,
            collapsible=False,
            limit=5,
        ))
