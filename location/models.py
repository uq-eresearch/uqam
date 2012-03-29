from django.db import models


class Place(models.Model):
    country = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=40, blank=True)
    australian_state = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=150)

    is_corrected = models.BooleanField(default=False,
            help_text="Has someone manually"
            "moved the marker to it's correct location.")
    gn_name = models.CharField(max_length=100,
            help_text="GeoNames Name", blank=True)
    gn_id = models.CharField(max_length=20,
            help_text="GeoNames ID", blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return ' > '.join([self.country, self.region, self.name])

    @models.permalink
    def get_absolute_url(self):
        return ('place_detail', [str(self.id)])

    def get_geonames_url(self):
        if self.gn_id:
            return "http://www.geonames.org/%s" % self.gn_id
        else:
            return False

    def get_kml_coordinates(self):
        return "%s,%s,0" % (self.longitude, self.latitude)

    def geocode_net(self, force=False):
        """
        Lookup the latitude and longitude of this place with GeoNames

        Place must be saved after use. Set `force` to re-lookup the location.

        Can take a few seconds to return, since this uses a network request.
        """
        if self.gn_id and not force:
            return
        from utils import geocoders
        geonames = geocoders.GeoNamesWithId()
        place, geonameId, (lat, lng) = geonames.geocode('%s, %s' %
                                                (self.name, self.country,),
                                                exactly_one=False)[0]
        self.gn_name = place
        self.gn_id = geonameId
        self.latitude = lat
        self.longitude = lng

    def geocode(self, force=False):
        from geonames.models import Geoname
        country = Geoname.objects.countries(name__contains=self.country)[0]
        geonames = Geoname.objects.filter(name__icontains=self.name,
                country=country.country)
        if geonames:
            g = geonames[0]
            self.gn_name = g.name
            self.gn_id = g.geonameid
            p = g.point.split(',')
            self.longitude = float(p[0])
            self.latitude = float(p[1])

    @staticmethod
    def autocomplete_search_fields():
        return ("country__icontains", "region__icontains",
                "australian_state__icontains", "name__icontains")


class Region(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

