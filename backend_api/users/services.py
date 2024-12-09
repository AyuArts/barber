import re

from users.validators import phone_validator


def normalize_phone(value: str) -> str:
    """
    Преобразование номера телефона к формату 389999999999
    для записи в BD.

    :param value: str, номер телефона в формате +38 (999) 999 99 99
    """
    phone_validator(value)

    digits = clear_format_phone(value)
    return f"{digits}"  # вывод: 389999999999

def clear_format_phone(value: str) -> str:
    """
    Удаляем все символы, кроме цифр
    """
    digits = re.sub(r'\D', '', value)
    return digits


def format_phone(value: str) -> str:
    """
    Преобразование номера телефона из формата 380999999999 в +38 (099) 999 99 99
    для вывода.

    :param value: str, номер телефона в формате 380999999999
    :return: str, номер телефона в формате +38 (099) 999 99 99
    """
    digits = value
    match = re.fullmatch(r'38(\d{3})(\d{3})(\d{2})(\d{2})', digits)
    return f"+38 ({match.group(1)}) {match.group(2)} {match.group(3)} {match.group(4)}"

