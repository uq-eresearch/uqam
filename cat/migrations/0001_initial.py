# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MuseumObject'
        db.create_table('cat_museumobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registration_number', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('old_registration_number', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('other_number', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('functional_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.FunctionalCategory'])),
            ('artefact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.ArtefactType'], blank=True)),
            ('storage_section', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('storage_unit', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('storage_bay', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('storage_shelf_box_drawer', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('acquisition_date', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('acquisition_method', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('loan_status', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('access_status', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('cultural_bloc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.CulturalBloc'], null=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.Place'], null=True)),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='donated_objects', null=True, to=orm['cat.Person'])),
            ('donor_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='donated_objects_2', null=True, to=orm['cat.Person'])),
            ('how_donor_obtained', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('when_donor_obtained', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('photographer', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('collector', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collected_objects', null=True, to=orm['cat.Person'])),
            ('collector_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collected_objects_2', null=True, to=orm['cat.Person'])),
            ('how_collector_obtained', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('when_collector_obtained', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('how_source_obtained', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('maker_or_artist', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('site_name_number', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('raw_material', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('indigenous_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('recorded_use', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('assoc_cultural_group', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('circumference', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('cat', ['MuseumObject'])

        # Adding model 'FunctionalCategory'
        db.create_table('cat_functionalcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('cat', ['FunctionalCategory'])

        # Adding model 'CulturalBloc'
        db.create_table('cat_culturalbloc', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('cat', ['CulturalBloc'])

        # Adding model 'ArtefactType'
        db.create_table('cat_artefacttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('cat', ['ArtefactType'])

        # Adding model 'Place'
        db.create_table('cat_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('australian_state', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('cat', ['Place'])

        # Adding model 'Person'
        db.create_table('cat_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('cat', ['Person'])


    def backwards(self, orm):
        
        # Deleting model 'MuseumObject'
        db.delete_table('cat_museumobject')

        # Deleting model 'FunctionalCategory'
        db.delete_table('cat_functionalcategory')

        # Deleting model 'CulturalBloc'
        db.delete_table('cat_culturalbloc')

        # Deleting model 'ArtefactType'
        db.delete_table('cat_artefacttype')

        # Deleting model 'Place'
        db.delete_table('cat_place')

        # Deleting model 'Person'
        db.delete_table('cat_person')


    models = {
        'cat.artefacttype': {
            'Meta': {'object_name': 'ArtefactType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'cat.culturalbloc': {
            'Meta': {'object_name': 'CulturalBloc'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
            'how_collector_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
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
            'registration_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'site_name_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'storage_bay': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_section': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_shelf_box_drawer': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'storage_unit': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'when_collector_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'when_donor_obtained': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'cat.person': {
            'Meta': {'object_name': 'Person'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'cat.place': {
            'Meta': {'object_name': 'Place'},
            'australian_state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        }
    }

    complete_apps = ['cat']
