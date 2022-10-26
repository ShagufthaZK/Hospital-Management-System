# accounts/admin.py
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

#to create a custom admin console
class CustomUserAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin')
    search_fields = ('email','username')
    readonly_fields = ('date_joined','last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(CustomUser,CustomUserAdmin)