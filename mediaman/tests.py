"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase
from unittest import TestCase
from views import name_to_id


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def assertNameToId(self, id, name, path=None):
        testid = name_to_id(name, path)
        self.assertEqual(id, testid)

    def test_name_to_id(self):
        self.assertNameToId(1234, '1234.jpg')

        self.assertNameToId(12345, '12345.jpg')

        self.assertNameToId(12345, '12345_2.jpg')

        self.assertNameToId(12345, '12345.pdf')
        self.assertNameToId(12345, '12345.png')
        self.assertNameToId(12345, '12345.tiff')

    def test_name_to_id_with_path(self):
        self.assertNameToId(12345, 'condition.tiff',
                'S:\\scanneddocs\\12345\\')
        self.assertNameToId(12345, 'condition.tiff',
                'S:\\scanneddocs\\12345')

        self.assertNameToId(12345, 'condition.tiff',
                '/home/omad/files/12345/')
        self.assertNameToId(12345, 'condition.tiff',
                '/home/omad/files/12345')

    def test_multiple_ids(self):
        ids = name_to_id('source file.pdf', '/home/files/123-132')
        expected = range(123, 132+1)
        self.assertEqual(expected, ids)
