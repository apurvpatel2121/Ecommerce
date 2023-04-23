from django.contrib import admin
from accounts.models import Account
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email',)
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account,UserAdmin)