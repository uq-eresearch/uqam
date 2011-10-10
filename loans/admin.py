from django.contrib import admin
from models import LoanAgreement, LoanItem, Client

class LoanItemInline(admin.TabularInline):
    model = LoanItem
    raw_id_fields = ('item',)

class LoanAgreementAdmin(admin.ModelAdmin):
    inlines = [
            LoanItemInline,
    ]
    model = LoanAgreement
    raw_id_fields = ('approved_by', 'prepared_by',)


admin.site.register(LoanAgreement, LoanAgreementAdmin)
admin.site.register(Client)
