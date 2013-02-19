from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals
from django.db import models
from mediaman.models import ArtefactRepresentation

# From http://stackoverflow.com/questions/1466827/ --
#
# Prevent interactive question about wanting a superuser created.  (This code
# has to go in this otherwise empty "models" module so that it gets 
# processed by the "syncdb" command during database creation.)
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')


# Create our own test user automatically.

def create_testuser(app, created_models, verbosity, **kwargs):
    if not settings.DEBUG:
        return
    try:
        auth_models.User.objects.get(username='admin')
    except auth_models.User.DoesNotExist:
        print '*' * 80
        print 'Creating test user -- login: admin, password: test'
        print '*' * 80
        assert auth_models.User.objects.create_superuser(
            'admin', 'd.ayers@uq.edu.au', 'test')
    else:
        print 'Test user already exists.'

signals.post_syncdb.connect(create_testuser,
    sender=auth_models, dispatch_uid='common.models.create_testuser')


class SiteConfiguration(models.Model):
    new_acquisition = models.ForeignKey('cat.MuseumObject',
        help_text="Use magnifying glass selector, the number displayed is an 'id' not a 'registration number'")
    new_acquisition_text = models.TextField(blank=True)
    new_acquisition_image = models.ForeignKey(ArtefactRepresentation, null=True)
    
    class Meta:
        verbose_name_plural = "Site configuration"
