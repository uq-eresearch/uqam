from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard


class UQAMDashboard(Dashboard):
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        self.children.append(modules.AppList(
            title=_('Catalogue'),
            column=1,
            collapsible=False,
            models=('cat.models.MuseumObject', 'parties.*', 'location.*',
                'loans.models.LoanAgreement', 'condition.*',
                'subcollections.*'),
            exclude=('django.contrib.*', 'djcelery.*', 'reports.*'),
        ))

        self.children.append(modules.AppList(
            title='Data dictionary',
            column=1,
            models=('cat.models.*', 'loans.models.LoanPurpose'),
            exclude=('cat.models.MuseumObject',)
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            column=1,
            collapsible=True,
            models=('django.contrib.*', 'djcelergy.*', 'reports.*',
                'dataimport.*', 'mediaman.*'),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            column=2,
            collapsible=False,
            limit=5,
        ))

        self.children.append(modules.LinkList(
            layout='inline',
            title=_('Admin tools'),
            column=2,
            children=(
                ['Upload media', '/mediaman/bulk_upload/'],
                ['Filter/query items', '/admin/cat/museumobject/search'],
            )
        ))
