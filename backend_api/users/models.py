from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Кастомный пользователь с добавлением роли.
    """
    ROLE_CHOICES = [
        ('student', 'Ученик'),
        ('teacher', 'Преподаватель'),
        ('model', 'Модель')
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name='Роль пользователя'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

