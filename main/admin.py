from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from . import models

class CustomUserAdmin(UserAdmin):
    pass

class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)


# Register your models here.
admin.site.register(models.Coupon)
admin.site.register(models.UserProfile)
admin.site.register(models.CustomUser, CustomUserAdmin)

