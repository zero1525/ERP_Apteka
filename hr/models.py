from django.db import models
from django.conf import settings

class Employees(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile', verbose_name="Аккаунт пользователя")
    avatar = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name="Фото")
    POSITION_CHOICES = (
        ('MANAGER', 'Менеджер'),
        ('PHARMACIST', 'Фармацевт'),
        ('CASHIER', 'Кассир'),
        ('WAREHOUSE_WORKER', 'Работник склада'),
        ('OTHER', 'Другое'),)   
    position = models.CharField(max_length=255, choices=POSITION_CHOICES)
    space = models.ForeignKey('space.Space', on_delete=models.CASCADE, related_name='employees')
    branch = models.ForeignKey('space.Branch', on_delete=models.CASCADE, related_name='employees')
    experience = models.PositiveIntegerField(verbose_name="Опыт работы (лет)", default=0)
    contact_info = models.TextField(blank=True, null=True, verbose_name="Контактная информация")
    skills = models.TextField(blank=True, null=True, verbose_name="Навыки и компетенции")
    iin = models.CharField(max_length=12, unique=True, verbose_name="ИИН паспорта", blank=True, null=True)
    year_of_birth = models.DateField(verbose_name="Год рождения", blank=True, null=True)
    hire_date = models.DateField(verbose_name="Дата найма", blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата", blank=True, null=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.position} - {self.space.name} - {self.contact_info}"


    

