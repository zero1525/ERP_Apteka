from django.db import models
from space.models import Space, Branch
from recepts.models import Recepts

class Stock(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='stocks', verbose_name="Аптека")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='stocks', verbose_name="Филиал")
    recept = models.ForeignKey(Recepts, on_delete=models.CASCADE, related_name='stocks', verbose_name="Лекарство")
    bathch_number = models.CharField(max_length=100, verbose_name="Номер партии")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена в этом филиале")
    delivery_date = models.DateField(verbose_name="дата доставки", auto_now=False, auto_now_add=False)
    manufactary_date = models.DateField(verbose_name = "Дата изготовления", auto_now=False, auto_now_add=False)
    expire_date = models.DateField(verbose_name="Срок годности", blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name="Доступно для продажи")

    def save (self, *args, **kwargs):
        if self.quantity == 0:
            self.avilable = False
        else:  
            self.avilable = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Остаток на складе"
        verbose_name_plural = "Остатки на складах"
        unique_together = ('branch', 'recept', 'bathch_number')

    def __str__(self):
        return f"{self.recept.name} в {self.branch.name}"


class Supplier(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='suppliers', verbose_name="Аптека")
    name = models.CharField(max_length=255, verbose_name="Название поставщика")
    description = models.TextField(blank=True, null=True, verbose_name="Описание поставщика")
    contact_info = models.TextField(blank=True, null=True, verbose_name="Контактная информация")

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name
    
class InventoryDocument(models.Model):
    DOC_TYPES = (
        ('INCOME', 'Приход от поставщика'),
        ('WRITE_OFF', 'Списание (брак/порча)'),
        ('RETURN', 'Возврат поставщику'),
    )
    
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    doc_type = models.CharField(choices=DOC_TYPES, max_length=10, verbose_name="Тип документа")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.CharField(max_length=50, verbose_name="Номер документа")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_posted = models.BooleanField(default=False, verbose_name="Проведен")

    class Meta:
        verbose_name = "Документ движения товара"
        verbose_name_plural = "Документы движения товара"

    def __str__(self):
        return f"{self.get_doc_type_display()} №{self.number} от {self.date.strftime('%Y-%m-%d')}"
    
class InventoryItem(models.Model):
    document = models.ForeignKey(InventoryDocument, on_delete=models.CASCADE, related_name='items')
    recept = models.ForeignKey(Recepts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    batch_number = models.CharField(max_length=100, verbose_name="Номер партии")
    expire_date = models.DateField(verbose_name="Срок годности", blank=True, null=True)
    
    class Meta:
        verbose_name = "Позиция документа"
        verbose_name_plural = "Позиции документов"

    def __str__(self):
        return f"{self.recept.name} x {self.quantity} в документе {self.document.number}"