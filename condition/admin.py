from django.contrib import admin
from models import ConditionReport, ConservationAction, Deaccession
from models import Conservator


class ConditionReportAdmin(admin.ModelAdmin):
    model = ConditionReport
    raw_id_fields = ('item','report_author')

class ConservationActionAdmin(admin.ModelAdmin):
    model = ConservationAction
    raw_id_fields = ('item','conservator')

class DeaccessionAdmin(admin.ModelAdmin):
    model = Deaccession
    raw_id_fields = ('item','person')


admin.site.register(ConditionReport, ConditionReportAdmin)
admin.site.register(ConservationAction, ConservationActionAdmin)
admin.site.register(Deaccession)
admin.site.register(Conservator)
