from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.user.models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'groups'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined')

# Reemplaza el modelo UserAdmin predeterminado por tu clase personalizada
admin.site.register(User, UserAdmin)
