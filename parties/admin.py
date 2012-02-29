from django.contrib import admin
from models import Person
from models import Maker
from models import MuseumStaff
from models import Client
from common.adminactions import merge_selected


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'comments',)
    search_fields = ['name', 'comments']
    filter_horizontal = ['related_documents']
    actions = [merge_selected]
admin.site.register(Person, PersonAdmin)


class MakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')
    search_fields = ('name', 'comment')
admin.site.register(Maker, MakerAdmin)


admin.site.register(Client)


class MuseumStaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'comments')
    search_fields = ('name', 'comments')
    model = MuseumStaff
admin.site.register(MuseumStaff, MuseumStaffAdmin)
