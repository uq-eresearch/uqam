from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard


class UQAMDashboard(Dashboard):
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        self.children.append(modules.AppList(
            title=_('Catalogue'),
            column=1,
            collapsible=False,
            models=('cat.models.MuseumObject', 'parties.*',
                    'loans.models.LoanAgreement', 'condition.*',
                    'subcollections.*'),
            exclude=('django.contrib.*', 'djcelery.*', 'location.*'),
        ))

        self.children.append(modules.LinkList(
            title=_('Geo-location'),
            column=1,
            children=(
                ['Geo-locations', '/admin/location/globalregion/jstree'],
            )
        ))

#        self.children.append(modules.ModelList(
#            title=_('Geo-location'),
#            column=1,
#            models=('location.models.GlobalRegion', 'location.models.Country',
#                'location.models.StateProvince', 'location.models.RegionDistrict',
#                'location.models.Locality', 'location.models.Place', 'location.models.Region'),
#        ))

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
            models=('django.contrib.*',
                    'djcelergy.*', 'mediaman.*', 'common.*'),
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
#               ['New acquisition', '/admin/common/siteconfiguration'],
                ['Bulk update storage locations', '/admin/cat/museumobject/upload_storagelocations'],
                ['Update new acquisition', '/admin/common/siteconfiguration/1/']
            )
        ))
