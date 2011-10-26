from django.contrib import admin
from models import ConditionReport, ConservationAction, Deaccession
from models import Conservator


class ConditionReportAdmin(admin.ModelAdmin):
    model = ConditionReport
    list_display = ('item','condition','date')
    list_filter = ('condition','date','report_author')
    raw_id_fields = ('report_author',)
    readonly_fields = ('item',)

class ConservationActionAdmin(admin.ModelAdmin):
    model = ConservationAction
    list_display = ('item','date','action','conservator')
    list_filter = ('date','action','conservator')
    raw_id_fields = ('conservator',)
    readonly_fields = ('item',)

class DeaccessionAdmin(admin.ModelAdmin):
    model = Deaccession
    raw_id_fields = ('person',)
    readonly_fields = ('item',)

class ConservatorAdmin(admin.ModelAdmin):
    model = Conservator
    list_display = ('__unicode__','organisation')


admin.site.register(ConditionReport, ConditionReportAdmin)
admin.site.register(ConservationAction, ConservationActionAdmin)
admin.site.register(Deaccession, DeaccessionAdmin)
admin.site.register(Conservator, ConservatorAdmin)
