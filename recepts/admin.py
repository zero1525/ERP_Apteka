from django.contrib import admin
from .models import Recepts, Category, Manufacturer, Barcode
from django.utils.html import format_html

class BarcodeInline(admin.TabularInline):
    model = Barcode
    extra = 1
    fields = ('code', 'volume', 'unitmeas')
    

   
@admin.register(Recepts)
class ReceptsAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_image', 'name', 'category', 'is_prescription_required', 'created_at')
    list_filter = ('category', 'is_prescription_required', 'manufacturer')
    search_fields = ('name', 'description', )
    readonly_fields = ('display_image', 'created_at', 'updated_at')
    inlines = [BarcodeInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'manufacturer', 'description', )
        }),
        ('Визуализация и статус', {
            'fields': ('image', 'display_image', 'is_prescription_required')
        }),
        ('Системная информация', {
            'classes': ('collapse',), 
            'fields': ('created_at', 'updated_at'),
        }),
    )
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "Нет фото"
    
    display_image.short_description = "Превью"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    fieldsets = (
        ("Основная информация", {
            'fields': ('name', 'slug', 'spaces')
        }),
    )
    
@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name', 'country')
    fieldsets = (
        ("Основная информация", {
            'fields': ('name', 'description', 'country', 'spaces')
        }),
    )