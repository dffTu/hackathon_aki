from django.core.mail import send_mail
from hackathon_aki import config
import datetime

MAX_LENGTH = {
    'email': 50,
    'password': 25,
    'first_name': 50,
    'last_name': 50,
    'middle_name': 50,
    'phone_number': 15,
    'position': 30,
    'juridical_name': 30,
    'inn': 15,
    'name': 30,
    'short_description': 1000,
    'description': 10000,
    'text': 5000
}


CHARSET = {
    'password': [
        lambda x: x.isascii() and x.isalnum(),
        lambda x: x in "!\"\#$%&\'()*+,-./:;<=>?@[\]^_`{|}~"
    ],
    'first_name': [
        lambda x: x.isalpha() and x.lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
    ],
    'last_name': [
        lambda x: x.isalpha() and x.lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
    ],
    'middle_name': [
        lambda x: x.isalpha() and x.lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
    ],
    'phone_number': [
        lambda x: x.isascii() and (x.isdigit() or x in '+()-'),
    ],
    'position': [
        lambda x: x.isprintable(),
    ],
    'juridical_name': [
        lambda x: x.isprintable(),
    ],
    'inn': [
        lambda x: x.isdigit() or x.isspace(),
    ],
    'name': [
        lambda x: x.isprintable(),
    ],
    'short_description': [
        lambda x: x.isprintable(),
    ],
    'description': [
        lambda x: x.isprintable(),
    ],
    'text': [
        lambda x: x.isprintable(),
    ],
}

weekdays = ['M', 'T', 'W', 'T', 'F', 'S', 'S']


class Day:
    def __init__(self, date, state):
        self.day = date.day
        self.weekday = date.weekday()
        self.state = state


def validate_length(field_names: list[str], form_data, error_log: dict[str, list[str]]) -> bool:
    is_valid = True
    for field_name in field_names:
        if len(form_data[field_name]) > MAX_LENGTH[field_name]:
            error_log[field_name].append(f'Превышено максимальное число символов {MAX_LENGTH[field_name]}')
            is_valid = False

    return is_valid


def validate_charset(field_names: list[str], form_data, error_log: dict[str, list[str]]) -> bool:
    is_valid = True
    for field_name in field_names:
        for char in form_data[field_name]:
            if True not in list(map(lambda x: x(char), CHARSET[field_name])):
                error_log[field_name].append(f'Символ \'{char}\' запрещён для этого поля')
                is_valid = False
                break

    return is_valid


def send_email_for_verify(request, email, verification_code):
    send_mail(
        "Подтверждение E-mail адреса",
        f"Перейдите по ссылке для подтверждения: {request.build_absolute_uri()[:-len(request.path)]}/email_verification/{verification_code}/",
        config.EMAIL_LOGIN,
        [email],
        fail_silently=False,
    )
