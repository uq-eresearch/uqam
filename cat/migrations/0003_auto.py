# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'CulturalBloc', fields ['name']
        db.create_index('cat_culturalbloc', ['name'])

        # Adding M2M table for field related_documents on 'MuseumObject'
        db.create_table('cat_museumobject_related_documents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('museumobject', models.ForeignKey(orm['cat.museumobject'], null=False)),
            ('document', models.ForeignKey(orm['mediaman.document'], null=False))
        ))
        db.create_unique('cat_museumobject_related_documents', ['museumobject_id', 'document_id'])

        # Adding M2M table for field related_documents on 'Person'
        db.create_table('cat_person_related_documents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['cat.person'], null=False)),
            ('document', models.ForeignKey(orm['mediaman.document'], null=False))
        ))
        db.create_unique('cat_person_related_documents', ['person_id', 'document_id'])


    def backwards(self, orm):
        
        # Removing index on 'CulturalBloc', fields ['name']
        db.delete_index('cat_culturalbloc', ['name'])

        # Removing M2M table for field related_documents on 'MuseumObject'
        db.delete_table('cat_museumobject_related_documents')

        # Removing M2M table for field related_documents on 'Person'
        db.delete_table('cat_person_related_documents')


    models = {
        'cat.artefacttype': {
            'Meta': {'object_name': 'ArtefactType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'cat.culturalbloc': {
            'Meta': {'object_name': 'CulturalBloc'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'cat.functionalcategory': {
            'Meta': {'object_name': 'FunctionalCategory'},
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
            'circumference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collector': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collected_objects'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'collector_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collected_objects_2'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cultural_bloc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.CulturalBloc']", 'null': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donated_objects'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'donor_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donated_objects_2'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'functional_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.FunctionalCategory']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'how_collector_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'how_donor_obtained': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'how_source_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indigenous_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'loan_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maker_or_artist': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'old_registration_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'other_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.Place']", 'null': 'True'}),
            'raw_material': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'recorded_use': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'reg_counter': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'registration_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_museumobjects'", 'symmetrical': 'False', 'to': "orm['mediaman.Document']"}),
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
            'Meta': {'object_name': 'Person'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_people'", 'symmetrical': 'False', 'to': "orm['mediaman.Document']"})
        },
        'cat.place': {
            'Meta': {'object_name': 'Place'},
            'australian_state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'mediaman.document': {
            'Meta': {'object_name': 'Document'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['cat']
