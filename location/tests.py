from django.test import TestCase

from models import GlobalRegion, Country, StateProvince, RegionDistrict, Locality
from admin_views import move, perform_move, calc_field_changes



class MergeTest(TestCase):
    fixtures = ['geolocations.json']


    def test_move(self):
        pass