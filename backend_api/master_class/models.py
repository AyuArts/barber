from django.db import models
from django.conf import settings

class MasterClass(models.Model):
    """
    Модель мастер-класса, содержащая информацию о названии, дате и участниках.
    """
    name = models.CharField(max_length=100, verbose_name='Название мастер-класса')
    date = models.DateField(verbose_name='Дата проведения')

    max_students = models.PositiveIntegerField(default=30)
    max_teachers = models.PositiveIntegerField(default=5)
    max_models = models.PositiveIntegerField(default=30)

    # Связи с пользователями
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='masterclass_students',
        limit_choices_to={'role': 'student'},
        blank=True,
        verbose_name='Ученики'
    )
    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='masterclass_teachers',
        limit_choices_to={'role': 'teacher'},
        blank=True,
        verbose_name='Преподаватели'
    )

    model = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='masterclass_models',
        limit_choices_to={'role': 'model'},
        blank=True,
        verbose_name='Модели'
    )





    def clean(self):
        """
        Проверка, что у мастер-класса есть хотя бы один преподаватель и один ученик.
        """
        from django.core.exceptions import ValidationError
        if not self.teachers.exists():
            raise ValidationError('Мастер-класс должен иметь хотя бы одного преподавателя.')
        if not self.students.exists():
            raise ValidationError('Мастер-класс должен иметь хотя бы одного ученика.')

    def __str__(self):
        return f"{self.name} - {self.date}"

    class Meta:
        verbose_name = 'Мастер-класс'
        verbose_name_plural = 'Мастер-классы'
        ordering = ['-date']  # Сортировка по дате (новые первыми)
