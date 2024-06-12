from django.contrib import admin
from .models import AttendanceManagerModel, WOR_date, WeekAttendanceRoleManager
# Register your models here.

class WeekAttendanceRoleManagerAdmin(admin.ModelAdmin):
    list_display = ('week_id', 'users_group', 'wor_leader', 'wor_engager')
    list_filter = ('users_group', 'week_id',)

class AttendanceManagerModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'person', 'user_status')
    list_filter = ('date',)
admin.site.register(AttendanceManagerModel, AttendanceManagerModelAdmin)
admin.site.register(WOR_date)
admin.site.register(WeekAttendanceRoleManager, WeekAttendanceRoleManagerAdmin)