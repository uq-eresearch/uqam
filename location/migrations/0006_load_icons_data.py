# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

icons_data = {
    "Australia": ("images/places/australia-thumb.jpg", "Kang Kang/Eagle carving | Unknown maker(s) |  Aurukun, Queensland | Donated by Reverend William MacKenzie, 1959"),
    "Pacific": ("images/places/pacific-thumb.jpg", "Malagan mask | Unknown maker(s) | New Ireland, Papua New Guinea | Foundation Donation, c1947"),
    "Asia": ("images/places/asia-thumb.jpg", "Child’s hat | Unknown maker(s) | Chiang Mai Province, Thailand | Purchased from Mrs Joy Martin, 1979"),
    "Africa": ("images/places/africa-thumb.jpg", "Sandstone bowl  | Unknown maker(s) | Botswana, Africa | Donated by Dr Coeli Geefhuysen, 2004"),
    "Europe": ("images/places/europe-thumb.jpg", "Stone axe | Unknown maker(s) | Furze Platt,  United Kingdom"),
    "Americas": ("images/places/americas-thumb.jpg", "Beaded shoulder bag | Unknown maker(s) | Attributed to Woodland Nations, United States of Americaira | Purchased from Church of England Board of Missions, 1967"),
    "Middle East": ("images/places/middleeast-thumb.jpg", "NONE"),
}


class Migration(DataMigration):

    def forwards(self, orm):
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        "Write your forwards methods here."
        for name, data in icons_data.items():
            gr = orm['location.GlobalRegion'].objects.get(name=name)
            gr.icon_path = data[0]
            gr.icon_title = data[1]
            gr.save()

    def backwards(self, orm):
        "Write your backwards methods here."

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
            'icon_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'icon_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
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
    symmetrical = True
