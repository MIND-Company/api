from django.core import validators


class PhoneValidator(validators.RegexValidator):
    regex = r"^\+[0-9]{11}$"
    message = "Введите корректный номер телефона. Номер состоит из знака '+' в начале строки и 11 цифр без пробелов"
    flags = 0
