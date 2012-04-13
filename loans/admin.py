from django.contrib import admin
from models import LoanAgreement, LoanItem, LoanPurpose
from parties.models import Client
from common.admin import UndeleteableModelAdmin
from common.adminactions import merge_selected


class LoanItemInline(admin.TabularInline):
    model = LoanItem
    raw_id_fields = ('item',)


class ClientInline(admin.StackedInline):
    model = Client


class LoanAgreementAdmin(UndeleteableModelAdmin):
    inlines = [
            LoanItemInline  # , ClientInline
    ]
    model = LoanAgreement
    list_display = ('id', 'client', 'date_borrowed',
                    'return_date', 'approved_by', 'loan_type')
    list_filter = ('client', 'date_borrowed', 'return_date', 'loan_type')
    raw_id_fields = ('approved_by', 'prepared_by', )


admin.site.register(LoanAgreement, LoanAgreementAdmin)


class LoanPurposeAdmin(admin.ModelAdmin):
    list_display = ('purpose', 'definition')
    actions = [merge_selected]

admin.site.register(LoanPurpose, LoanPurposeAdmin)
