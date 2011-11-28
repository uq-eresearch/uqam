from geopy import geocoders
from geopy import util

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        from django.utils import simplejson as json

class GeoNamesWithId(geocoders.GeoNames):
    """
    Use GeoNames geocoder, also returning geonamesId with location
    """
    def __init__(self, *args, **kwargs):
        super(GeoNamesWithId, self).__init__(*args, **kwargs)
# FIXME: Don't hard code
        self.url = "http://ws.geonames.org/searchJSON?user=uqamcatalogue&%s"

    def parse_json(self, page, exactly_one):
        if not isinstance(page, basestring):
            page = util.decode_page(page)
            
        doc = json.loads(page)
        places = doc.get('geonames', [])
        
        if not places:
            return None
        
        if exactly_one and len(places) != 1:
            raise ValueError("Didn't find exactly one code! " \
                             "(Found %d.)" % len(places))
        
        def parse_code(place):
            latitude = place.get('lat', None)
            longitude = place.get('lng', None)
            if latitude and longitude:
                latitude = float(latitude)
                longitude = float(longitude)
            else:
                return None
            
            placename = place.get('name')
            state = place.get('adminCode1', None)
            country = place.get('countryCode', None)
            geonamesId = place.get('geonameId')
            
            location = ', '.join(filter(lambda x: bool(x),
                [placename, state, country]
            ))
            
            return (location, geonamesId, (latitude, longitude))
        
        if exactly_one:
            return parse_code(places[0])
        else:
            return [parse_code(place) for place in places]
