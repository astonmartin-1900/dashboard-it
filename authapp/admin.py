from django.urls import path
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserModel, GroupAdmin

class CustomUserAdmin(UserAdmin):
    def change_password_view(self, request, object_id, form_url='', extra_context=None):
        # Your code for the password change view goes here
        pass

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:object_id>/change_password/', self.admin_site.admin_view(self.change_password_view), name='auth_user_change_password'),
        ]
        return my_urls + urls

admin.site.register(UserModel, CustomUserAdmin)
admin.site.register(GroupAdmin)