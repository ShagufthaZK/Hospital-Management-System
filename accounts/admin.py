# accounts/admin.py
from django.contrib import admin
from .models import CustomUser, InsuranceClaim,Product, Cart
from .models import CustomUser, OTPMobileVerification, UserFiles
from django.contrib.auth.admin import UserAdmin

#to create a custom admin console
class CustomUserAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','user_type','is_approved')
    search_fields = ('email','username','user_type')
    readonly_fields = ('date_joined','last_login') #TODO: should user_type be immutable??
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(InsuranceClaim)
admin.site.register(OTPMobileVerification)
admin.site.register(UserFiles)#UserFiles
