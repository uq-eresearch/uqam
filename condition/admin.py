from django.contrib import admin
from models import ConditionReport, ConservationAction, Deaccession
from models import Conservator


class ConditionReportAdmin(admin.ModelAdmin):
    model = ConditionReport
    list_display = ('item','condition','date','report_author')
    list_filter = ('condition','date','report_author')
    raw_id_fields = ('report_author','item',)

class ConservationActionAdmin(admin.ModelAdmin):
    model = ConservationAction
    list_display = ('item','date','action','conservator')
    list_filter = ('date','action','conservator')
    raw_id_fields = ('conservator','item',)

class DeaccessionAdmin(admin.ModelAdmin):
    model = Deaccession
    list_display = ('item','date','person','reason')
    list_filter = ('date','person')
    raw_id_fields = ('person','item',)

class ConservatorAdmin(admin.ModelAdmin):
    model = Conservator
    list_display = ('__unicode__','organisation')


admin.site.register(ConditionReport, ConditionReportAdmin)
admin.site.register(ConservationAction, ConservationActionAdmin)
admin.site.register(Deaccession, DeaccessionAdmin)
admin.site.register(Conservator, ConservatorAdmin)
