from django.contrib import admin
from .models import AppUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # Removed 'date_joined' since it's not in the AppUser model
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active')
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(AppUser, AppUserAdmin)
