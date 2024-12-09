import re
from django.core.exceptions import ValidationError
from .message import *

def phone_validator(value: str) -> None:
    """
    Валидатор для проверки правильности ввода номера телефона.

    :param value: str, значение номера телефона
    :raises ValidationError: если номер не соответствует формату
    """
    regex = r'^\+38\s\(\d{3}\)\s\d{3}\s\d{2}\s\d{2}$'
    message_error = MESSAGE_ERROR_PHONE
    regex_validator(value, regex, message_error)

def regex_validator(value: str, regex: str, message_error: str) -> None:
    """
    Универсальный валидатор для проверки значения на соответствие регулярному выражению.

    :param value: str, значение, которое нужно проверить
    :param regex: str, регулярное выражение
    :param message_error: str, сообщение об ошибке
    :raises ValidationError: если значение не соответствует регулярному выражению или ошибка в регулярном выражении
    """
    try:
        if not re.match(regex, value):
            raise ValidationError(message_error)
    except re.error as error:
        raise ValidationError(MESSAGE_ERROR_REGEX.format(error=error))




def validate_image_extension(value):
    if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError(MESSAGE_ERROR_IMAGE_EXPANSION)

def validate_image_size(value):
    """
    Валидатор для проверки веса изображения.

    :param value: Загружаемый файл
    :raises ValidationError: Если размер файла превышает лимит
    """
    max_size_mb = 5  # Максимальный размер файла в МБ
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            MESSAGE_ERROR_IMAGE_SIZE,
            params={
                'max_size_mb': max_size_mb,
                'file_size': round(value.size / (1024 * 1024), 2)
            }
        )