from django.contrib import admin
from .models import User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        ('Основная информация', {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('full_name',)}),
        ('Права доступа', {'fields': ('is_staff', 'is_active')}),
    )

