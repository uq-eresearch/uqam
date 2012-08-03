# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Country.parent'
        db.alter_column('location_country', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.PROTECT, to=orm['location.GlobalRegion']))

        # Changing field 'RegionDistrict.parent'
        db.alter_column('location_regiondistrict', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.PROTECT, to=orm['location.StateProvince']))

        # Changing field 'StateProvince.parent'
        db.alter_column('location_stateprovince', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.PROTECT, to=orm['location.Country']))

        # Changing field 'Locality.parent'
        db.alter_column('location_locality', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(on_delete=models.PROTECT, to=orm['location.RegionDistrict']))

    def backwards(self, orm):

        # Changing field 'Country.parent'
        db.alter_column('location_country', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.GlobalRegion']))

        # Changing field 'RegionDistrict.parent'
        db.alter_column('location_regiondistrict', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.StateProvince']))

        # Changing field 'StateProvince.parent'
        db.alter_column('location_stateprovince', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Country']))

        # Changing field 'Locality.parent'
        db.alter_column('location_locality', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.RegionDistrict']))

    models = {
        'location.country': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('parent', 'slug'),)", 'object_name': 'Country'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'on_delete': 'models.PROTECT', 'to': "orm['location.GlobalRegion']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.globalregion': {
            'Meta': {'ordering': "['name']", 'object_name': 'GlobalRegion'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.locality': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('parent', 'slug'),)", 'object_name': 'Locality'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'on_delete': 'models.PROTECT', 'to': "orm['location.RegionDistrict']"}),
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
            'region': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'location.region': {
            'Meta': {'object_name': 'Region'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'location.regiondistrict': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('parent', 'slug'),)", 'object_name': 'RegionDistrict'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'on_delete': 'models.PROTECT', 'to': "orm['location.StateProvince']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'location.stateprovince': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('parent', 'slug'),)", 'object_name': 'StateProvince'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gn_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gn_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'on_delete': 'models.PROTECT', 'to': "orm['location.Country']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['location']