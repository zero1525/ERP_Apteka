from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Space(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name=("Описание аптеки"), help_text="Введите описание аптеки", blank=True, null=True)

    class Meta:
        verbose_name = ("Аптека")
        verbose_name_plural = ("Аптеки")

    def __str__(self):
        return self.name
   
class Branch(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("Филиал")
        verbose_name_plural = ("Филиалы")
    
    def __str__(self):
        return f"{self.name} - {self.address}"

class PhoneNumber(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='phone_numbers')
    operator = models.CharField(max_length=255, verbose_name=("Оператор связи"), help_text="Введите название оператора связи", blank=True, null=True)
    number = PhoneNumberField(verbose_name = ("Номер телефона"), help_text="Введите номер телефона", blank=True, null=True)

    
    class Meta:
        verbose_name = ("Номер телефона")
        verbose_name_plural = ("Номера телефонов")

    def __str__(self):
        return f"{self.operator}: {self.number}"

class SocialMedia(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='social_media')
    platform = models.CharField(max_length=255)
    url = models.URLField(verbose_name=("Ссылка на социальную сеть"), help_text="Введите ссылку на социальную сеть", blank=True, null=True)
    
    class Meta:
        verbose_name = ("Социальная сеть")
        verbose_name_plural = ("Социальные сети")

    def __str__(self):
        return f"{self.platform}: {self.url}"
    
