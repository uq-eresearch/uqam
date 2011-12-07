from django.contrib import admin
from models import LoanAgreement, LoanItem, Client, MuseumStaff
from common.admin import UndeleteableModelAdmin


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
admin.site.register(Client)

class MuseumStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'comments')
    search_fields = ('name', 'comments')
    model = MuseumStaff
admin.site.register(MuseumStaff, MuseumStaffAdmin)

