from django.test import TestCase

from models import GlobalRegion, Country, StateProvince, RegionDistrict, Locality
from admin_views import move, perform_move, calc_field_changes
from exceptions import IllegalMove


class MoveTest(TestCase):

    def setUp(self):
        print GlobalRegion.objects.all()
        self.new_parent = GlobalRegion.objects.get(name='Asia')
        self.orig_parent = GlobalRegion.objects.get(name='Australia')

        self.child = Country.objects.get(name='Australia', parent=self.gr_australia)

    def test_not_move_globalregions(self):
        with self.assertRaises(IllegalMove):
            self.orig_parent.moveto_parent(self.new_parent)

    def test_simple_country_move(self):
        num_in_child = self.child.museumobject_set.count()
        num_in_new_parent = self.new_parent.museumobject_set.count()
        num_in_orig_parent = self.orig_parent.museumobject_set.count()

        # Perform the move
        self.child.moveto_parent(self.new_parent)
        self.child.save()

        # Check parent field updated
        self.assertEqual(self.new_parent, self.child.parent)

        # Check counts
        self.assertEqual(num_in_child,
            self.child.museumobject_set.count())
        self.assertEqual(num_in_new_parent + num_in_child,
            self.new_parent.museumobject_set.count())
        self.assertEqual(num_in_orig_parent - num_in_child,
            self.orig_parent.museumobject_set.count())
