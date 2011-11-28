# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.template.defaultfilters import slugify

class Migration(DataMigration):

    def forwards(self, orm):
        """
        Calculate the slugged name of the category, for use in urls
        """
        for category in orm.Category.objects.all():
            category.slug = slugify(category.name)
            category.save()

    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'cat.artefacttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ArtefactType'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'see_also': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'cat.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cat.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cat.culturalbloc': {
            'Meta': {'ordering': "['name']", 'object_name': 'CulturalBloc'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'cat.functionalcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'FunctionalCategory'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'cat.museumobject': {
            'Meta': {'ordering': "['registration_number']", 'object_name': 'MuseumObject'},
            'access_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'acquisition_date': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'acquisition_method': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'artefact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.ArtefactType']", 'blank': 'True'}),
            'assoc_cultural_group': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cat.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'circumference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collected_objects'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'collector_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collected_objects_2'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cultural_bloc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.CulturalBloc']", 'null': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'donor_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects_2'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'exhibition_history': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'functional_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.FunctionalCategory']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'how_collector_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'how_donor_obtained': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'how_source_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'indigenous_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'is_public_comment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'loan_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'maker_or_artist': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'old_registration_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'other_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.Place']", 'null': 'True'}),
            'private_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'raw_material': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'recorded_use': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'reg_counter': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'registration_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_museumobjects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['mediaman.Document']"}),
            'site_name_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'storage_bay': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_section': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_shelf_box_drawer': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_unit': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'when_collector_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'when_donor_obtained': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cat.person': {
            'Meta': {'ordering': "['name']", 'object_name': 'Person'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'related_people'", 'blank': 'True', 'to': "orm['mediaman.Document']"})
        },
        'cat.place': {
            'Meta': {'object_name': 'Place'},
            'australian_state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_corrected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'cat.region': {
            'Meta': {'object_name': 'Region'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'mediaman.document': {
            'Meta': {'object_name': 'Document'},
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['cat']
