from django.contrib.admin import ModelAdmin
from django.contrib import admin
from common.models import SiteConfiguration

class UndeleteableModelAdmin(ModelAdmin):
    """Disable deleting any objects through the admin"""
    def get_actions(self, request):
        actions = super(UndeleteableModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class SiteConfigurationAdmin(admin.ModelAdmin):
    raw_id_fields = ('homepage_item',)



admin.site.register(SiteConfiguration, SiteConfigurationAdmin)