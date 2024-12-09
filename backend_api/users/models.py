from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from .services import  normalize_phone


class User(AbstractUser):
    """
    Кастомный пользователь с добавлением роли.
    """
    ROLE_CHOICES = [
        ('student', 'Ученик'),
        ('teacher', 'Преподаватель'),
        ('model', 'Модель'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='Роль пользователя'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Additionally(models.Model):
    """
    Дополнительные данные пользователя.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="additional_info")
    phone = models.CharField(max_length=15, unique=True, verbose_name="Телефон")
    age = models.PositiveSmallIntegerField(verbose_name="Возраст")
    avatar = models.ImageField(upload_to='media/avatars/', blank=True, null=True, verbose_name="Аватар")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")

    def clean(self):
        """
        Нормализация номера телефона перед сохранением.
        """
        self.phone = normalize_phone(self.phone)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Дополнительная информация"
        verbose_name_plural = "Дополнительные информации"
