from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AdminUser, Customer


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'country', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    list_filter = ('country',)
