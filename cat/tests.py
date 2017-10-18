"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.

It some point it will be necessary to split this into multiple files. See 
http://www.pioverpi.net/2010/03/10/organizing-django-tests-into-folders/
http://djangosnippets.org/snippets/1972/
http://dougalmatthews.com/articles/2010/jan/20/testing-your-first-django-app/
"""

from django.test import TestCase
from django.test.client import Client



class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_museumobjects_list(self):
        # Issue a GET request
        response = self.client.get('/item/')

        self.assertEqual(response.status_code, 200)

    def test_museumobjects_view(self):
        # Issue a GET request
        response = self.client.get('/item/1')

        self.assertEqual(response.status_code, 404)

