from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	list_display = ('id', 'username', 'email', 'role', 'is_active', 'is_staff')
	list_filter = ('role', 'is_active', 'is_staff')
	fieldsets = UserAdmin.fieldsets + (
		('Role & Audit', {'fields': ('role', 'created_at', 'updated_at')}),
	)
	readonly_fields = ('created_at', 'updated_at')
