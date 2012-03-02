# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'LoanAgreement'
        db.create_table('loans_loanagreement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ref', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parties.Client'])),
            ('date_borrowed', self.gf('django.db.models.fields.DateField')()),
            ('return_date', self.gf('django.db.models.fields.DateField')()),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='approved_by', to=orm['parties.MuseumStaff'])),
            ('prepared_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prepared_by', to=orm['parties.MuseumStaff'])),
            ('loan_type', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('special_loan_conditions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('purpose', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loans.LoanPurpose'], null=True)),
            ('returned', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('loans', ['LoanAgreement'])

        # Adding model 'LoanPurpose'
        db.create_table('loans_loanpurpose', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('purpose', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('loans', ['LoanPurpose'])

        # Adding model 'LoanItem'
        db.create_table('loans_loanitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('loan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loans.LoanAgreement'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.MuseumObject'])),
            ('out_condition', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('return_condition', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('loans', ['LoanItem'])

        # Adding unique constraint on 'LoanItem', fields ['loan', 'item']
        db.create_unique('loans_loanitem', ['loan_id', 'item_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'LoanItem', fields ['loan', 'item']
        db.delete_unique('loans_loanitem', ['loan_id', 'item_id'])

        # Deleting model 'LoanAgreement'
        db.delete_table('loans_loanagreement')

        # Deleting model 'LoanPurpose'
        db.delete_table('loans_loanpurpose')

        # Deleting model 'LoanItem'
        db.delete_table('loans_loanitem')


    models = {
        'cat.accessstatus': {
            'Meta': {'object_name': 'AccessStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'cat.acquisitionmethod': {
            'Meta': {'object_name': 'AcquisitionMethod'},
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
            'recorded_use': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'reg_counter': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'reg_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'registered_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parties.MuseumStaff']", 'null': 'True'}),
            'registration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'registration_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_museumobjects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['mediaman.Document']"}),
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
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'how': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'loans.loanagreement': {
            'Meta': {'ordering': "['id']", 'object_name': 'LoanAgreement'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'approved_by'", 'to': "orm['parties.MuseumStaff']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parties.Client']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_borrowed': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cat.MuseumObject']", 'through': "orm['loans.LoanItem']", 'symmetrical': 'False'}),
            'loan_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'prepared_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prepared_by'", 'to': "orm['parties.MuseumStaff']"}),
            'purpose': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loans.LoanPurpose']", 'null': 'True'}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'return_date': ('django.db.models.fields.DateField', [], {}),
            'returned': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'special_loan_conditions': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'loans.loanitem': {
            'Meta': {'unique_together': "(('loan', 'item'),)", 'object_name': 'LoanItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.MuseumObject']"}),
            'loan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loans.LoanAgreement']"}),
            'out_condition': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'return_condition': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'loans.loanpurpose': {
            'Meta': {'object_name': 'LoanPurpose'},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
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
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'parties.client': {
            'Meta': {'ordering': "['name']", 'object_name': 'Client'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'phone1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'town_suburb': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'}),
            'related_documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'related_people'", 'blank': 'True', 'to': "orm['mediaman.Document']"})
        }
    }

    complete_apps = ['loans']
