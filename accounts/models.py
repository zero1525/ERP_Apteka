from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager

class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-date_joined",)
    ROLE_CHOICES = (
        ("admin", "Администратор"),       # Видит всё в рамках своего Space
        ("manager", "Менеджер"),          # Управляет филиалом
        ("support", "Служба поддержки"),  # Глобальный доступ (для тебя)
        ("user", "Кассир/Пользователь"),   # Только продажи
    )
    # Убираем username, так как логин будет по email
    username = None
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    phone_number = PhoneNumberField(verbose_name="Номер телефона", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user", verbose_name="Роль")
    # СВЯЗИ ДЛЯ MULTI-TENANCY
    space = models.ForeignKey(
        'space.Space', 
        on_delete=models.CASCADE, 
        related_name='users', 
        null=True, 
        blank=True, 
        verbose_name="Сеть аптек"
    )
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"] # Email и Password запрашиваются по умолчанию

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"