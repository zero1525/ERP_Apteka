from django.db import models

class HeaderCheck(models.Model):
    space = models.ForeignKey('space.Space', on_delete=models.CASCADE, related_name='header_checks', verbose_name="Аптека")
    branch = models.ForeignKey('space.Branch', on_delete=models.CASCADE, related_name='header_checks', verbose_name="Филиал")
    number = models.CharField(max_length=50, verbose_name="Номер чека")
    number_kassa = models.CharField(max_length=50, verbose_name="Номер кассы")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма", default=0.00)
    


    class Meta:
        verbose_name = "Заголовок чека"
        verbose_name_plural = "Заголовки чеков"

    def __str__(self):
        return f"Чек {self.number} от {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
class CheckItem(models.Model):
    header_check = models.ForeignKey(HeaderCheck, on_delete=models.CASCADE, related_name='items', verbose_name="Заголовок чека")
    recept = models.ForeignKey('recepts.Recepts', on_delete=models.PROTECT, related_name='check_items', verbose_name="Лекарство")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")   
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая цена")
   

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Позиция чека"
        verbose_name_plural = "Позиции чеков"

    def __str__(self):
        return f"{self.recept.name} x {self.quantity} в чеке {self.header_check.number}"
