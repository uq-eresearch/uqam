# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AcquisitionMethod'
        db.create_table('cat_acquisitionmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('cat', ['AcquisitionMethod'])

        # Adding model 'LoanStatus'
        db.create_table('cat_loanstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('cat', ['LoanStatus'])

        # Adding model 'AccessStatus'
        db.create_table('cat_accessstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('cat', ['AccessStatus'])

        # Adding model 'Obtained'
        db.create_table('cat_obtained', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('how', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('cat', ['Obtained'])

        # Adding model 'MuseumObject'
        db.create_table('cat_museumobject', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('registration_number', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('old_registration_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('other_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('reg_counter', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('functional_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.FunctionalCategory'])),
            ('artefact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.ArtefactType'], blank=True)),
            ('storage_section', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('storage_unit', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('storage_bay', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('storage_shelf_box_drawer', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('acquisition_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('acquisition_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.AcquisitionMethod'], null=True)),
            ('loan_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.LoanStatus'], null=True)),
            ('access_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.AccessStatus'], null=True)),
            ('reg_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('registered_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parties.MuseumStaff'], null=True)),
            ('registration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cultural_bloc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.CulturalBloc'], null=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Place'], null=True)),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='donated_objects', null=True, to=orm['parties.Person'])),
            ('donor_2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='donated_objects_2', null=True, to=orm['parties.Person'])),
            ('how_donor_obtained', self.gf('django.db.models.fields.related.ForeignKey')(related_name='donor_obtained', null=True, to=orm['cat.Obtained'])),
            ('when_donor_obtained', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('photographer', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('collector', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='collected_objects', null=True, to=orm['parties.Person'])),
            ('collector_2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='collected_objects_2', null=True, to=orm['parties.Person'])),
            ('how_collector_obtained', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collector_obtained', null=True, to=orm['cat.Obtained'])),
            ('when_collector_obtained', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('how_source_obtained', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source_obtained', null=True, to=orm['cat.Obtained'])),
            ('maker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parties.Maker'], null=True, blank=True)),
            ('manufacture_technique', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('site_name_number', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('raw_material', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('indigenous_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recorded_use', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('assoc_cultural_group', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('exhibition_history', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_illustrated', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('artefact_illustrated', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public_comment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('private_comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('significance', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('depth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('circumference', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('cat', ['MuseumObject'])

        # Adding M2M table for field category on 'MuseumObject'
        db.create_table('cat_museumobject_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('museumobject', models.ForeignKey(orm['cat.museumobject'], null=False)),
            ('category', models.ForeignKey(orm['cat.category'], null=False))
        ))
        db.create_unique('cat_museumobject_category', ['museumobject_id', 'category_id'])

        # Adding M2M table for field related_documents on 'MuseumObject'
        db.create_table('cat_museumobject_related_documents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('museumobject', models.ForeignKey(orm['cat.museumobject'], null=False)),
            ('document', models.ForeignKey(orm['mediaman.document'], null=False))
        ))
        db.create_unique('cat_museumobject_related_documents', ['museumobject_id', 'document_id'])

        # Adding model 'FunctionalCategory'
        db.create_table('cat_functionalcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('definition', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('cat', ['FunctionalCategory'])

        # Adding model 'CulturalBloc'
        db.create_table('cat_culturalbloc', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, db_index=True)),
            ('definition', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('cat', ['CulturalBloc'])

        # Adding model 'ArtefactType'
        db.create_table('cat_artefacttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('definition', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('see_also', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal('cat', ['ArtefactType'])

        # Adding model 'Category'
        db.create_table('cat_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['cat.Category'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('cat', ['Category'])

        # Adding unique constraint on 'Category', fields ['slug', 'parent']
        db.create_unique('cat_category', ['slug', 'parent_id'])

        # Adding unique constraint on 'Category', fields ['name', 'parent']
        db.create_unique('cat_category', ['name', 'parent_id'])

        # Adding M2M table for field suggested_artefact_types on 'Category'
        db.create_table('cat_category_suggested_artefact_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['cat.category'], null=False)),
            ('artefacttype', models.ForeignKey(orm['cat.artefacttype'], null=False))
        ))
        db.create_unique('cat_category_suggested_artefact_types', ['category_id', 'artefacttype_id'])

        # Adding model 'Reference'
        db.create_table('cat_reference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('museum_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.MuseumObject'])),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('publications_details', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('cat', ['Reference'])

        # Adding model 'PhotoRecord'
        db.create_table('cat_photorecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('museum_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.MuseumObject'])),
            ('phototype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cat.PhotoType'])),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('cat', ['PhotoRecord'])

        # Adding model 'PhotoType'
        db.create_table('cat_phototype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phototype', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('cat', ['PhotoType'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Category', fields ['name', 'parent']
        db.delete_unique('cat_category', ['name', 'parent_id'])

        # Removing unique constraint on 'Category', fields ['slug', 'parent']
        db.delete_unique('cat_category', ['slug', 'parent_id'])

        # Deleting model 'AcquisitionMethod'
        db.delete_table('cat_acquisitionmethod')

        # Deleting model 'LoanStatus'
        db.delete_table('cat_loanstatus')

        # Deleting model 'AccessStatus'
        db.delete_table('cat_accessstatus')

        # Deleting model 'Obtained'
        db.delete_table('cat_obtained')

        # Deleting model 'MuseumObject'
        db.delete_table('cat_museumobject')

        # Removing M2M table for field category on 'MuseumObject'
        db.delete_table('cat_museumobject_category')

        # Removing M2M table for field related_documents on 'MuseumObject'
        db.delete_table('cat_museumobject_related_documents')

        # Deleting model 'FunctionalCategory'
        db.delete_table('cat_functionalcategory')

        # Deleting model 'CulturalBloc'
        db.delete_table('cat_culturalbloc')

        # Deleting model 'ArtefactType'
        db.delete_table('cat_artefacttype')

        # Deleting model 'Category'
        db.delete_table('cat_category')

        # Removing M2M table for field suggested_artefact_types on 'Category'
        db.delete_table('cat_category_suggested_artefact_types')

        # Deleting model 'Reference'
        db.delete_table('cat_reference')

        # Deleting model 'PhotoRecord'
        db.delete_table('cat_photorecord')

        # Deleting model 'PhotoType'
        db.delete_table('cat_phototype')


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
            'artefact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.ArtefactType']", 'blank': 'True'}),
            'assoc_cultural_group': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cat.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'category_illustrated': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'circumference': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'collector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collected_objects'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'collector_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collected_objects_2'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cultural_bloc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.CulturalBloc']", 'null': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'donor_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'donated_objects_2'", 'null': 'True', 'to': "orm['parties.Person']"}),
            'exhibition_history': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'functional_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cat.FunctionalCategory']"}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'how_collector_obtained': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collector_obtained'", 'null': 'True', 'to': "orm['cat.Obtained']"}),
            'how_donor_obtained': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donor_obtained'", 'null': 'True', 'to': "orm['cat.Obtained']"}),
            'how_source_obtained': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source_obtained'", 'null': 'True', 'to': "orm['cat.Obtained']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
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
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
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

    complete_apps = ['cat']
