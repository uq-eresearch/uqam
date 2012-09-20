from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from exceptions import IllegalMove, SameLevelMove, WrongLevelMove


slug_length = 50


class LocationBase(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(help_text='Unique identifier. May be used in URLs.', max_length=slug_length)
    description = models.CharField(max_length=255, blank=True)

    gn_name = models.CharField(max_length=100,
            help_text="GeoNames Name", blank=True)
    gn_id = models.CharField(max_length=20,
            help_text="GeoNames ID", blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        abstract = True

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:slug_length]
        super(LocationBase, self).save(*args, **kwargs)

    def get_kml_coordinates(self):
        return "%s,%s,0" % (self.longitude, self.latitude)

    @models.permalink
    def get_absolute_url(self):
        #import ipdb; ipdb.set_trace()
        contenttype = ContentType.objects.get_for_model(self).model
        return ('view_geoloc', [str(contenttype), str(self.id)])

    def get_parents(self):
        if hasattr(self, 'parent'):
            parent = self.parent
            return parent.get_parents() + [parent]
        else:
            return []

    def moveto_parent(self, new_parent):
        self._validate_move(new_parent)
        return self._perform_move(new_parent)

    def _validate_move(self, new_parent):
        if not hasattr(self, 'parent'):
            # Top level of tree, cannot move
            raise IllegalMove()

        if type(self) == type(new_parent):
            # Parent cannot be of same type
            raise SameLevelMove

        parent_field = self._meta.get_field_by_name('parent')[0]
        req_parent_type = parent_field.rel.to

        if req_parent_type != type(new_parent):
            # new_parent is wrong type for this class
            raise WrongLevelMove

    def _perform_move(self, new_parent):
        # Check for conflicting children and merge if they exist
        if hasattr(new_parent, 'children') and \
            new_parent.children.filter(slug=self.slug):

            to_merge = new_parent.children.get(slug=self.slug)
            return self.merge(to_merge, self)
        else:
            # Simple move
            self.parent = new_parent
            self.save()

            # Update museumobjects
            field_changes = calc_field_changes(self)
            self.museumobject_set.update(**field_changes)
            return self

    @staticmethod
    def merge(target, old):
        if hasattr(old, 'children'):
            # Deal with all the children of old
            targets_children = [child.slug for child in target.children.all()]

            for child in old.children.all():
                if child.slug in targets_children:
                    # Need to merge
                    match = target.children.get(slug=child.slug)
                    LocationBase.merge(match, child)
                else:
                    # Simply move child
                    child.parent = target
                    child.save()

                    changes = calc_field_changes(target)
                    child.museumobject_set.update(**changes)

        # now that old has no children
        # Actually merge the two
        changes = calc_field_changes(target)
        old.museumobject_set.update(**changes)
        if old.museumobject_set.exists():
            raise Exception
        else:
            old.delete()

        return target


def find_mo_field_name(element):
    return element._meta.concrete_model.museumobject_set.\
            related.field.name


def calc_field_changes(element):
    """
    Walk up the tree of geo-locations, finding the new parents

    These will be set onto all the museumobjects.
    """
    fieldname = find_mo_field_name(element)
    field_changes = {fieldname: element.id}
    if hasattr(element, 'parent'):
        field_changes.update(
            calc_field_changes(element.parent))
    return field_changes


class GlobalRegion(LocationBase):
    icon_path = models.CharField(max_length=255, blank=True,
        help_text="Relative path to icon")
    icon_title = models.CharField(max_length=255, blank=True,
        help_text="Icon title, displayed on browse page")

    class Meta(LocationBase.Meta):
        pass


class Country(LocationBase):
    parent = models.ForeignKey(GlobalRegion, related_name='children',
        verbose_name='Global region', on_delete=models.PROTECT)

    class Meta(LocationBase.Meta):
        verbose_name_plural = 'countries'
        unique_together = ('parent', 'slug')


class StateProvince(LocationBase):
    parent = models.ForeignKey(Country, related_name='children',
        verbose_name='Country', on_delete=models.PROTECT)

    class Meta(LocationBase.Meta):
        unique_together = ('parent', 'slug')


class RegionDistrict(LocationBase):
    parent = models.ForeignKey(StateProvince, related_name='children',
        verbose_name='State/province', on_delete=models.PROTECT)

    class Meta(LocationBase.Meta):
        unique_together = ('parent', 'slug')


class Locality(LocationBase):
    parent = models.ForeignKey(RegionDistrict, related_name='children',
        verbose_name='Region/district', on_delete=models.PROTECT)

    class Meta(LocationBase.Meta):
        verbose_name_plural = 'localities'
        unique_together = ('parent', 'slug')


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

    @staticmethod
    def autocomplete_search_fields():
        return ("country__icontains", "region__icontains",
                "australian_state__icontains", "name__icontains")


class Region(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
