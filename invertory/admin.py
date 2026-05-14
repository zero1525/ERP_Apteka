from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Supplier, Stock, InventoryDocument, InventoryItem

class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1
    autocomplete_fields = ['recept'] # Требует search_fields в ReceptsAdmin

@admin.register(InventoryDocument)
class InventoryDocumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'doc_type', 'branch', 'date', 'status_tag')
    list_filter = ('doc_type', 'is_posted', 'branch')
    inlines = [InventoryItemInline]
    readonly_fields = ('is_posted',)

    def status_tag(self, obj):
        if obj.is_posted:
            return format_html('<b style="color: green;">✔ Проведен</b>')
        return format_html('<b style="color: orange;">⏳ Черновик</b>')
    status_tag.short_description = "Статус"

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'space', 'contact_info')
    search_fields = ('name', 'contact_info')
    # Исправлено: в модели у тебя 'space', а не 'spaces'
    list_filter = ('space',) 
    fieldsets = (
        ("Основная информация", {
            'fields': ('name', 'space', 'contact_info')
        }),
        ("Описание", {
            'classes': ('collapse',), 
            'fields': ('description',)
        }),
    )

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    # Исправлено: используем 'expire_date' и 'available' (учитывая опечатку в save)
    list_display = ('recept', 'quantity', 'price', 'expiration_status', 'branch')
    list_filter = ('branch', 'expire_date', 'available')
    search_fields = ('recept__name',)
    autocomplete_fields = ['recept']
    
    fieldsets = (
        ("Информация о товаре", {
            'fields': ('recept', 'space', 'branch', 'bathch_number')
        }),
        ("Склад и цена", {
            'fields': ('quantity', 'price', 'expire_date', 'available')
        }),
    )

    def expiration_status(self, obj):
        if not obj.expire_date:
            return "—"
        
        today = timezone.now().date()
        days_left = (obj.expire_date - today).days
        
        if days_left < 0:
            return format_html('<span style="color: red; font-weight: bold;">{} (Просрочен!)</span>', obj.expire_date)
        elif days_left <= 30:
            return format_html('<span style="color: orange; font-weight: bold;">{} (Срочно реализовать)</span>', obj.expire_date)
        
        return obj.expire_date
    expiration_status.short_description = "Срок годности"