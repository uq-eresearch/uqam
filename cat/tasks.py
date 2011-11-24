from celery.decorators import task
from models import Place

@task
def GeocodePlace(place_id):
    """
    Add geocoded location data to a `Place`
    """
    p = Place.objects.get(id=place_id)
    p.geocode()
    p.save()
