from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class MasterClass(models.Model):
    """
    Модель мастер-класса, содержащая информацию о названии, дате и участниках.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Название мастер-класса',
        help_text='Введите название мастер-класса'
    )
    date = models.DateField(
        verbose_name='Дата проведения',
        help_text='Укажите дату проведения мастер-класса'
    )
    content = models.TextField(
        max_length=500,
        verbose_name='Описание',
        help_text='Опишите содержание мастер-класса'
    )

    max_students = models.PositiveIntegerField(
        default=30,
        validators=[MaxValueValidator(50)],
        verbose_name='Максимальное количество учеников',
        help_text='Максимальное количество участников в роли учеников'
    )
    max_teachers = models.PositiveIntegerField(
        default=5,
        validators=[MaxValueValidator(10)],
        verbose_name='Максимальное количество преподавателей',
        help_text='Максимальное количество участников в роли преподавателей'
    )
    max_models = models.PositiveIntegerField(
        default=30,
        validators=[MaxValueValidator(50)],
        verbose_name='Максимальное количество моделей',
        help_text='Максимальное количество участников в роли моделей'
    )

    # Связи с пользователями
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='masterclass_students',
        limit_choices_to={'role': 'student'},
        blank=True,
        verbose_name='Ученики',
        help_text='Укажите учеников, которые будут участвовать'
    )
    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='masterclass_teachers',
        limit_choices_to={'role': 'teacher'},
        blank=True,
        verbose_name='Преподаватели',
        help_text='Укажите преподавателей, которые будут участвовать'
    )
    models = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='masterclass_models',
        limit_choices_to={'role': 'model'},
        blank=True,
        verbose_name='Модели',
        help_text='Укажите моделей, которые будут участвовать'
    )

    def clean(self):
        """
        Проверка, что у мастер-класса есть хотя бы один преподаватель и один ученик.
        """
        if not self.teachers.exists():
            raise ValidationError('Мастер-класс должен иметь хотя бы одного преподавателя.')
        if not self.students.exists():
            raise ValidationError('Мастер-класс должен иметь хотя бы одного ученика.')
        if self.students.count() > self.max_students:
            raise ValidationError('Превышено максимальное количество учеников.')
        if self.teachers.count() > self.max_teachers:
            raise ValidationError('Превышено максимальное количество преподавателей.')
        if self.models.count() > self.max_models:
            raise ValidationError('Превышено максимальное количество моделей.')

    def __str__(self):
        return f"{self.name} - {self.date}"

    class Meta:
        verbose_name = 'Мастер-класс'
        verbose_name_plural = 'Мастер-классы'
        ordering = ['-date']  # Сортировка по дате (новые первыми)

class Comentary(models.Model):
    """
    Комментарии для мастер-класса.
    """
    masterclass = models.ForeignKey(
        MasterClass,
        on_delete=models.CASCADE,
        related_name='comentaries',
        verbose_name='Мастер-класс'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Введите текст комментария'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Комментарий к {self.masterclass.name}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

class Recall(models.Model):
    """
    Отзыв на мастер-класс.
    """
    masterclass = models.ForeignKey(
        MasterClass,
        on_delete=models.CASCADE,
        related_name='recalls',
        verbose_name='Мастер-класс'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка',
        help_text='Оцените мастер-класс от 1 до 5'
    )
    feedback = models.TextField(
        verbose_name='Отзыв',
        help_text='Оставьте отзыв о мастер-классе'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Отзыв на {self.masterclass.name} - {self.rating} звёзд"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']