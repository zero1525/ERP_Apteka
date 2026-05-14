from django.contrib import admin
from .models import HeaderCheck, CheckItem
from django.db.models import Sum

class CheckItemInline(admin.TabularInline):
    model = CheckItem
    extra = 1
    # Убедись, что в модели CheckItem поле называется 'recept' или 'product'
    fields = ('recept', 'quantity', 'price', 'get_sum') 
    readonly_fields = ('get_sum',) # Если эти поля есть в модели

    # ЭТОТ МЕТОД ОПИСЫВАЕТ ТВОЮ ОШИБКУ E035
    def get_sum(self, obj):
        if obj and obj.price and obj.quantity:
            return obj.price * obj.quantity
        return 0
    get_sum.short_description = "Сумма"

@admin.register(HeaderCheck)
class HeaderCheckAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'branch', 'total_amount_display')
    list_filter = ('date', 'branch')
    inlines = [CheckItemInline]
    
    readonly_fields = ('total_amount','date')
    
    fieldsets = (
        ("Основная информация", {
            'fields': ('number',  'branch')
        }),
        ("Финансы", {
            'fields': ('total_amount',),
        }),
    )

    def total_amount_display(self, obj):
        return f"{obj.total_amount} сом"
    total_amount_display.short_description = "Итоговая сумма"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        
        # Считаем сумму всех позиций: (количество * цена)
        # Если в модели CheckItem нет метода для этого, считаем вручную через цикл:
        total = 0
        for item in form.instance.items.all():
            total += (item.price * item.quantity)
            
        form.instance.total_amount = total
        form.instance.save()