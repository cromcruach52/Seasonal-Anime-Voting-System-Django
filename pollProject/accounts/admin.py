from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'region', 'gender', 'age']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('region', 'gender', 'age')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)