from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

UserAdmin.list_display += ('is_active', 'is_superuser',)
UserAdmin.fieldsets += (('Extra Fields', {'fields': ('birthday', 'cellphone', 'national_code')}),)

admin.site.register(User, UserAdmin)
