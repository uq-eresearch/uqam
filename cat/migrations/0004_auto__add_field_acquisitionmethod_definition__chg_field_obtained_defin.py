# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AcquisitionMethod.definition'
        db.add_column('cat_acquisitionmethod', 'definition', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Changing field 'Obtained.definition'
        db.alter_column('cat_obtained', 'definition', self.gf('django.db.models.fields.TextField')())

        # Adding field 'AccessStatus.definition'
        db.add_column('cat_accessstatus', 'definition', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'LoanStatus.definition'
        db.add_column('cat_loanstatus', 'definition', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Deleting field 'RecordStatus.description'
        db.delete_column('cat_recordstatus', 'description')

        # Adding field 'RecordStatus.definition'
        db.add_column('cat_recordstatus', 'definition', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'AcquisitionMethod.definition'
        db.delete_column('cat_acquisitionmethod', 'definition')

        # Changing field 'Obtained.definition'
        db.alter_column('cat_obtained', 'definition', self.gf('django.db.models.fields.CharField')(max_length=150))

        # Deleting field 'AccessStatus.definition'
        db.delete_column('cat_accessstatus', 'definition')

        # Deleting field 'LoanStatus.definition'
        db.delete_column('cat_loanstatus', 'definition')

        # Adding field 'RecordStatus.description'
        db.add_column('cat_recordstatus', 'description', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Deleting field 'RecordStatus.definition'
        db.delete_column('cat_recordstatus', 'definition')


    models = {
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
            'method': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cat.artefacttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ArtefactType'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'see_also': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'cat.category': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('slug', 'parent'), ('name', 'parent'))", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cat.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
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
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cultural_bloc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.CulturalBloc']", 'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'donor_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects_2'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'exhibition_history': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'functional_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.FunctionalCategory']", 'null': 'True', 'blank': 'True'}),
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
            'registered_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parties.MuseumStaff']", 'null': 'True'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'registration_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mediaman.Document']", 'null': 'True', 'blank': 'True'}),
            'significance': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'site_name_number': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
        'mediaman.document': {
            'Meta': {'object_name': 'Document'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5sum': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
