from django.contrib.admin import ModelAdmin

class UndeleteableModelAdmin(ModelAdmin):
    """Disable deleting any objects through the admin"""
    def get_actions(self, request):
        actions = super(UndeleteableModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    def has_delete_permission(self, request, obj=None):
        return False
