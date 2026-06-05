from django.contrib import admin
from django.utils.html import format_html
from .models import Employees

@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('display_avatar', 'get_full_name', 'position', 'space', 'salary', 'hire_date')
    search_fields = ('user__full_name', 'user__email', 'iin', 'position')
    list_filter = ('space', 'position', 'hire_date')
    readonly_fields = ('display_avatar_large', 'hire_date')
    fieldsets = (
        ('Аккаунт и фото', {
            'fields': ('user', 'avatar', 'display_avatar_large')
        }),
        ('Профессиональные данные', {
            'fields': ('position', 'space', 'experience', 'salary', 'hire_date', 'branch')
        }),
        ('Личные данные', {
            'fields': ('iin', 'year_of_birth', 'contact_info', 'skills')
        }),
    )

    def display_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.avatar.url)
        return "Нет фото"
    display_avatar.short_description = "Фото"

    # Метод для отображения большого аватара в форме редактирования
    def display_avatar_large(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="150" height="150" style="border-radius: 10px;" />', obj.avatar.url)
        return "Фото не загружено"
    display_avatar_large.short_description = "Превью фото"

    # Метод для получения имени из связанной модели User
    def get_full_name(self, obj):
        return obj.user.full_name or obj.user.email
    get_full_name.short_description = "Сотрудник"

    # Чтобы зарплата подсвечивалась, если она не указана (опционально)
    def get_salary(self, obj):
        if not obj.salary:
            return format_html('<span style="color: red;">Не указана</span>')
        return f"{obj.salary} сом"
    get_salary.short_description = "Оклад"