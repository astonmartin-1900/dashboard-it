from django.contrib import admin
from .models import *
# Register your models here.
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id','action_group', 'creation_date', 'issue_name', 'deadline_date', 'get_assigned_user', 'action_status')
    list_display_links = ('id', 'issue_name')
    search_fields = ('issue_name',)
    list_editable = ('action_status',)
    list_filter = ('action_status', 'issue_name')

admin.site.register(ActionTaskManagerModel, ActionAdmin)
admin.site.register(AssignedToAction)