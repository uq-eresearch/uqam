from django.test import TestCase

from models import GlobalRegion, Country, StateProvince, RegionDistrict, Locality
from exceptions import IllegalMove, SameLevelMove, WrongLevelMove


class MoveTest(TestCase):
    fixtures = ['testlocations.json']

    def setUp(self):
        self.asia = GlobalRegion.objects.get(name='Asia')
        self.gr_australia = GlobalRegion.objects.get(name='Australia')

        self.country_australia = Country.objects.get(name='Australia', parent=self.gr_australia)
        self.country_thailand = Country.objects.get(name='Thailand', parent=self.asia)
        self.country_no_children = Country.objects.get(name='NoChildren', parent=self.gr_australia)

        self.stateprovince_1 = StateProvince.objects.get(name='Queensland',
            parent=self.country_australia)

        self.regiondistrict_1 = RegionDistrict.objects.get(name='SEQ',
            parent=self.stateprovince_1)

        self.locality_1 = Locality.objects.get(name='Brisbane',
            parent=self.regiondistrict_1)

    def test_cannot_move_globalregions(self):
        """
        Try moving a global region inside another global region
        """
        with self.assertRaises(IllegalMove):
            self.gr_australia.moveto_parent(self.asia)

    def test_cannot_move_to_same_level(self):
        """
        Try moving a country into another country
        """
        with self.assertRaises(SameLevelMove):
            self.country_australia.moveto_parent(self.country_thailand)

    def test_cannot_move_to_wrong_level(self):
        """
        Try (and fail) moving a StateProvince into a GlobalRegion
        """
        with self.assertRaises(WrongLevelMove):
            self.stateprovince_1.moveto_parent(self.asia)

    def test_move_locality(self):
        maleny = Locality.objects.get(name='Maleny')
        orig_parent = maleny.parent
        northern = RegionDistrict.objects.get(name='Northern')
        num_in_child = maleny.museumobject_set.count()
        num_in_new_parent = northern.museumobject_set.count()
        num_in_orig_parent = maleny.parent.museumobject_set.count()
#        import ipdb; ipdb.set_trace()
        child = maleny.moveto_parent(northern)

        # Check counts
        self.assertEqual(num_in_child,
            child.museumobject_set.count())
        self.assertEqual(num_in_new_parent + num_in_child,
            northern.museumobject_set.count())
        self.assertEqual(num_in_orig_parent - num_in_child,
            orig_parent.museumobject_set.count())


    def test_simple_country_move(self):
        """
        Move a country to another global region

        The country has linked museumobjects, but no children
        and no merge required.
        """
        child = Country.objects.get(name='NoChildren', parent=self.gr_australia)
        num_in_child = child.museumobject_set.count()
        num_in_new_parent = self.asia.museumobject_set.count()
        num_in_orig_parent = self.gr_australia.museumobject_set.count()

        # Perform the move
        child = child.moveto_parent(self.asia)

        # Check parent field updated
        self.assertEqual(self.asia, child.parent)

        # Check counts
        self.assertEqual(num_in_child,
            child.museumobject_set.count())
        self.assertEqual(num_in_new_parent + num_in_child,
            self.asia.museumobject_set.count())
        self.assertEqual(num_in_orig_parent - num_in_child,
            self.gr_australia.museumobject_set.count())

        self.assertTreeCounts(self.gr_australia)
        self.assertTreeCounts(self.asia)

    def test_simple_country_merge(self):
        """
        Move a country to another global region

        A country with the same name exists already, and both countries
        have some linked museum objects, so must be merged.
        """
        child = self.country_no_children
        old_parent = child.parent
        new_parent = GlobalRegion.objects.get(name='Europe')
        merge_target = Country.objects.get(name='NoChildren', parent=new_parent)

        num_in_child = child.museumobject_set.count()
        num_in_old_parent = old_parent.museumobject_set.count()
        num_in_new_parent = new_parent.museumobject_set.count()
        num_in_merge_target = merge_target.museumobject_set.count()

        # Perform the move
        child = child.moveto_parent(new_parent)

        # Check parent field updated
        self.assertEqual(new_parent, child.parent)

        # Check counts
        self.assertEqual(num_in_old_parent - num_in_child,
            old_parent.museumobject_set.count())
        self.assertEqual(num_in_new_parent + num_in_child,
            new_parent.museumobject_set.count())
        self.assertEqual(num_in_child + num_in_merge_target,
            merge_target.museumobject_set.count())
        self.assertTreeCounts(new_parent)
        self.assertTreeCounts(old_parent)

    def test_complex_country_merge(self):
        """
        Move a country to another global region

        A country with the same name exists already, and both countries
        have both linked museum objects and conflicting children, so must be merged.
        """
        child = Country.objects.get(name='Australia', parent=self.asia)
        old_parent = child.parent
        new_parent = GlobalRegion.objects.get(name='Australia')
        merge_target = Country.objects.get(name='Australia', parent=self.gr_australia)

        num_in_child = child.museumobject_set.count()
        num_in_old_parent = old_parent.museumobject_set.count()
        num_in_new_parent = new_parent.museumobject_set.count()
        num_in_merge_target = merge_target.museumobject_set.count()

        # Perform the move
        child = child.moveto_parent(new_parent)

        # Check parent field updated
        self.assertEqual(new_parent, child.parent)

        # Check counts
        self.assertEqual(num_in_old_parent - num_in_child,
            old_parent.museumobject_set.count())
        self.assertEqual(num_in_new_parent + num_in_child,
            new_parent.museumobject_set.count())
        self.assertEqual(num_in_child + num_in_merge_target,
            merge_target.museumobject_set.count())
        self.assertTreeCounts(new_parent)
        self.assertTreeCounts(old_parent)

    def move_country_with_children(self):
        """
        Move a country that countains children (and linked MOs)

        There is however no merging required
        """
        pass

    def assertTreeCounts(self, location):
        """
        Check that a there are at least as many MOs linked
        to a parent location as to it's children.
        """
        count = location.museumobject_set.count()

        if hasattr(location, 'children') and location.children.exists():
            child_count = 0
            for child in location.children.all():
                child_count += child.museumobject_set.count()
                self.assertTreeCounts(child)

            self.assertTrue(count >= child_count)


