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
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loans.Client'])),
            ('date_borrowed', self.gf('django.db.models.fields.DateField')()),
            ('return_date', self.gf('django.db.models.fields.DateField')()),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='approved_by', to=orm['cat.Person'])),
            ('prepared_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prepared_by', to=orm['cat.Person'])),
            ('loan_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('loan_purpose', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('special_loan_conditions', self.gf('django.db.models.fields.TextField')()),
            ('comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('loans', ['LoanAgreement'])

        # Adding model 'LoanItem'
        db.create_table('loans_loanitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('loan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['loans.LoanAgreement'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.MuseumObject'])),
            ('out_condition', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('return_condition', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('loans', ['LoanItem'])

        # Adding model 'Client'
        db.create_table('loans_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organisation', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('town_suburb', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone1', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('phone2', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('loans', ['Client'])


    def backwards(self, orm):
        
        # Deleting model 'LoanAgreement'
        db.delete_table('loans_loanagreement')

        # Deleting model 'LoanItem'
        db.delete_table('loans_loanitem')

        # Deleting model 'Client'
        db.delete_table('loans_client')


    models = {
        'cat.artefacttype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ArtefactType'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'see_also': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
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
            'circumference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collected_objects'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'collector_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collected_objects_2'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cultural_bloc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.CulturalBloc']", 'null': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'donor_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects_2'", 'null': 'True', 'to': "orm['cat.Person']"}),
            'functional_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.FunctionalCategory']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'how_collector_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'how_donor_obtained': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'how_source_obtained': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
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
        'loans.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'phone1': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'town_suburb': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'loans.loanagreement': {
            'Meta': {'object_name': 'LoanAgreement'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'approved_by'", 'to': "orm['cat.Person']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loans.Client']"}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'date_borrowed': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cat.MuseumObject']", 'through': "orm['loans.LoanItem']", 'symmetrical': 'False'}),
            'loan_purpose': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'loan_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'prepared_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prepared_by'", 'to': "orm['cat.Person']"}),
            'ref': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'return_date': ('django.db.models.fields.DateField', [], {}),
            'special_loan_conditions': ('django.db.models.fields.TextField', [], {})
        },
        'loans.loanitem': {
            'Meta': {'object_name': 'LoanItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.MuseumObject']"}),
            'loan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['loans.LoanAgreement']"}),
            'out_condition': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'return_condition': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'mediaman.document': {
            'Meta': {'object_name': 'Document'},
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['loans']
