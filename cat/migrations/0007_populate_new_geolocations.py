# -*- coding: utf-8 -*-
from south.v2 import DataMigration
from django.template.defaultfilters import slugify
import string
import random


def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))


class Migration(DataMigration):

    def get_or_create(self, model, name, parent, max_slug=50):
        slug = slugify(name)[:max_slug]
        try:
            obj = model.objects.get(slug=slug, parent=parent)
        except model.DoesNotExist:
            obj = model(name=name, slug=slug, parent=parent)
            obj.save()
        except Exception as e:
            print e

        return obj

    def forwards(self, orm):
        # Fix cultural blocs
        c = orm.CulturalBloc.objects.get(name="None")
        orm.MuseumObject.objects.filter(cultural_bloc=None).update(cultural_bloc=c)

        # Migrate to new geo-locations structure
        "Write your forwards methods here."
        for mo in orm.MuseumObject.objects.all():
            cultural_bloc = mo.cultural_bloc
            country = mo.place.country
            region = mo.place.region
            australian_state = mo.place.australian_state
            place_name = mo.place.name

            global_region, c = orm['location.GlobalRegion'].objects.get_or_create(
                name=cultural_bloc.name, description=cultural_bloc.definition,
                slug=slugify(cultural_bloc.name))
            country = self.get_or_create(orm['location.Country'], country, global_region)
            state_province = self.get_or_create(orm['location.StateProvince'], australian_state, country)
            region_district = self.get_or_create(orm['location.RegionDistrict'], region, state_province)
            locality = self.get_or_create(orm['location.Locality'], place_name, region_district)

            mo.global_region = global_region
            mo.country = country
            mo.state_province = state_province
            mo.region_district = region_district
            mo.locality = locality

            mo.save()

        orm.MuseumObject.objects.all().update(is_public_comment=True)
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

    def backwards(self, orm):
        "Write your backwards methods here."
        orm.MuseumObject.objects.all().update(global_region=None, country=None,
            state_province=None, region_district=None, locality=None)
#        for mo in orm.MuseumObject.objects.all():
#            mo.global_region = None
#            mo.country = None
#            mo.state_province = None
#            mo.region_district = None
#            mo.locality = None
#            mo.save()
        orm['location.GlobalRegion'].objects.all().delete()
        orm['location.Country'].objects.all().delete()
        orm['location.StateProvince'].objects.all().delete()
        orm['location.RegionDistrict'].objects.all().delete()
        orm['location.Locality'].objects.all().delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cat.accessstatus': {
            'Meta': {'object_name': 'AccessStatus'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cat.acquisitionmethod': {
            'Meta': {'object_name': 'AcquisitionMethod'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'preposition': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'cat.artefacttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ArtefactType'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'see_also': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'cat.category': {
            'Meta': {'ordering': "['parent__name', 'name']", 'unique_together': "(('slug', 'parent'), ('name', 'parent'))", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cat.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'suggested_artefact_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'categories'", 'null': 'True', 'to': "orm['cat.ArtefactType']"})
        },
        'cat.culturalbloc': {
            'Meta': {'ordering': "['name']", 'object_name': 'CulturalBloc'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'})
        },
        'cat.functionalcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'FunctionalCategory'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cat.loanstatus': {
            'Meta': {'object_name': 'LoanStatus'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cat.museumobject': {
            'Meta': {'ordering': "['registration_number']", 'object_name': 'MuseumObject'},
            'access_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.AccessStatus']", 'null': 'True'}),
            'acquisition_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'acquisition_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.AcquisitionMethod']", 'null': 'True'}),
            'artefact_illustrated': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'artefact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.ArtefactType']"}),
            'assoc_cultural_group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cat.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'category_illustrated': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'circumference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collected_objects'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'collector_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collected_objects_2'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Country']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cultural_bloc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.CulturalBloc']", 'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'donor_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects_2'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'exhibition_history': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'functional_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.FunctionalCategory']", 'null': 'True', 'blank': 'True'}),
            'global_region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.GlobalRegion']", 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'how_collector_obtained': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collector_obtained'", 'null': 'True', 'to': "orm['cat.Obtained']"}),
            'how_donor_obtained': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donor_obtained'", 'null': 'True', 'to': "orm['cat.Obtained']"}),
            'how_source_obtained': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source_obtained'", 'null': 'True', 'to': "orm['cat.Obtained']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indigenous_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'is_public_comment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'loan_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.LoanStatus']", 'null': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Locality']", 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'maker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parties.Maker']", 'null': 'True', 'blank': 'True'}),
            'manufacture_technique': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'old_registration_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'other_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Place']", 'null': 'True'}),
            'private_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'raw_material': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'record_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.RecordStatus']", 'null': 'True', 'blank': 'True'}),
            'recorded_use': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'reg_counter': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'reg_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'region_district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.RegionDistrict']", 'null': 'True', 'blank': 'True'}),
            'registered_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parties.MuseumStaff']", 'null': 'True'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'registration_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mediaman.Document']", 'null': 'True', 'blank': 'True'}),
            'significance': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'site_name_number': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state_province': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.StateProvince']", 'null': 'True', 'blank': 'True'}),
            'storage_bay': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_section': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_shelf_box_drawer': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_unit': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'when_collector_obtained': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'when_donor_obtained': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cat.obtained': {
            'Meta': {'object_name': 'Obtained'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'how': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cat.photorecord': {
            'Meta': {'object_name': 'PhotoRecord'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'museum_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.MuseumObject']"}),
            'phototype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.PhotoType']"})
        },
        'cat.phototype': {
            'Meta': {'object_name': 'PhotoType'},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phototype': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cat.recordstatus': {
            'Meta': {'object_name': 'RecordStatus'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cat.reference': {
            'Meta': {'object_name': 'Reference'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'museum_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.MuseumObject']"}),
            'publications_details': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'location.country': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'Country'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.GlobalRegion']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.globalregion': {
            'Meta': {'object_name': 'GlobalRegion'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.locality': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'Locality'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.RegionDistrict']"}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.place': {
            'Meta': {'ordering': "['id']", 'object_name': 'Place'},
            'australian_state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_corrected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'location.regiondistrict': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'RegionDistrict'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.StateProvince']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.stateprovince': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'StateProvince'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Country']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'mediaman.document': {
            'Meta': {'object_name': 'Document'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'document_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5sum': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'original_filedate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'original_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'parties.maker': {
            'Meta': {'ordering': "['name']", 'object_name': 'Maker'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'parties.museumstaff': {
            'Meta': {'ordering': "['name']", 'object_name': 'MuseumStaff'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'parties.person': {
            'Meta': {'ordering': "['name']", 'object_name': 'Person'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'related_people'", 'blank': 'True', 'to': "orm['mediaman.Document']"})
        }
    }

    complete_apps = ['cat']
    symmetrical = True
