# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table('location_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gn_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('gn_id', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.GlobalRegion'])),
        ))
        db.send_create_signal('location', ['Country'])

        # Adding unique constraint on 'Country', fields ['parent', 'slug']
        db.create_unique('location_country', ['parent_id', 'slug'])

        # Adding model 'RegionDistrict'
        db.create_table('location_regiondistrict', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gn_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('gn_id', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.StateProvince'])),
        ))
        db.send_create_signal('location', ['RegionDistrict'])

        # Adding unique constraint on 'RegionDistrict', fields ['parent', 'slug']
        db.create_unique('location_regiondistrict', ['parent_id', 'slug'])

        # Adding model 'GlobalRegion'
        db.create_table('location_globalregion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gn_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('gn_id', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('location', ['GlobalRegion'])

        # Adding model 'StateProvince'
        db.create_table('location_stateprovince', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gn_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('gn_id', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Country'])),
        ))
        db.send_create_signal('location', ['StateProvince'])

        # Adding unique constraint on 'StateProvince', fields ['parent', 'slug']
        db.create_unique('location_stateprovince', ['parent_id', 'slug'])

        # Adding model 'Locality'
        db.create_table('location_locality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gn_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('gn_id', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.RegionDistrict'])),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal('location', ['Locality'])

        # Adding unique constraint on 'Locality', fields ['parent', 'slug']
        db.create_unique('location_locality', ['parent_id', 'slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Locality', fields ['parent', 'slug']
        db.delete_unique('location_locality', ['parent_id', 'slug'])

        # Removing unique constraint on 'StateProvince', fields ['parent', 'slug']
        db.delete_unique('location_stateprovince', ['parent_id', 'slug'])

        # Removing unique constraint on 'RegionDistrict', fields ['parent', 'slug']
        db.delete_unique('location_regiondistrict', ['parent_id', 'slug'])

        # Removing unique constraint on 'Country', fields ['parent', 'slug']
        db.delete_unique('location_country', ['parent_id', 'slug'])

        # Deleting model 'Country'
        db.delete_table('location_country')

        # Deleting model 'RegionDistrict'
        db.delete_table('location_regiondistrict')

        # Deleting model 'GlobalRegion'
        db.delete_table('location_globalregion')

        # Deleting model 'StateProvince'
        db.delete_table('location_stateprovince')

        # Deleting model 'Locality'
        db.delete_table('location_locality')


    models = {
        'location.country': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'Country'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.GlobalRegion']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.globalregion': {
            'Meta': {'object_name': 'GlobalRegion'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.locality': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'Locality'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        'location.region': {
            'Meta': {'object_name': 'Region'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'location.regiondistrict': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'RegionDistrict'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.StateProvince']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.stateprovince': {
            'Meta': {'unique_together': "(('parent', 'slug'),)", 'object_name': 'StateProvince'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Country']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['location']