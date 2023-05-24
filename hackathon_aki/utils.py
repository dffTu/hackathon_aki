from django.core.mail import send_mail
from hackathon_aki import config
from platforms.models import FreeSlot
import datetime

MAX_LENGTH = {
    'email': 50,
    'password': 50,
    'first_name': 50,
    'last_name': 50,
    'middle_name': 50,
    'phone_number': 15,
    'position': 50,
    'juridical_name': 50,
    'inn': 15,
    'name': 50,  # platform name
    'short_description': 1000,  # short platform description
    'description': 10000,  # platform description
    'text': 10000  # comment length
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
        lambda x: x.isprintable() or x.isascii(),
    ],
    'juridical_name': [
        lambda x: x.isprintable() or x.isascii(),
    ],
    'inn': [
        lambda x: x.isdigit() or x.isspace(),
    ],
    'name': [
        lambda x: x.isprintable() or x.isascii(),
    ],
    'short_description': [
        lambda x: x.isprintable() or x.isascii(),
    ],
    'description': [
        lambda x: x.isprintable() or x.isascii(),
    ],
    'text': [
        lambda x: x.isprintable() or x.isascii(),
    ],
}

weekdays = ['M', 'T', 'W', 'T', 'F', 'S', 'S']


class Slot:
    def __init__(self, date, state):
        self.day = date.day
        self.weekday = date.weekday()
        self.state = state


def build_slots(today, platform_id):
    slots = []
    free_slots = FreeSlot.objects.filter(platform_id=platform_id)
    for week in range(5):
        week_slots = []
        for weekday in range(7):
            delta = weekday - today.weekday() + week * 7
            if delta < 0:
                state = 'previous'
            elif delta == 0:
                state = 'today'
            else:
                state = 'future'
            tmp_date = datetime.date.today() + datetime.timedelta(delta)
            if not free_slots.filter(date=tmp_date).exists():
                if state != 'previous':
                    state = 'booked'
            week_slots.append(Slot(tmp_date, state))
        slots.append(week_slots, platform_id)
    return slots


def validate_length(field_names: list[str], required_fields: list[str], form_data, error_log: dict[str, list[str]]) -> bool:
    is_valid = True
    for field_name in field_names:
        if field_name not in form_data:
            continue

        if len(form_data[field_name]) > MAX_LENGTH[field_name]:
            error_log[field_name].append(f'Превышено максимальное число символов {MAX_LENGTH[field_name]}')
            is_valid = False

    for field_name in required_fields:
        if field_name not in form_data or len(form_data[field_name]) == 0:
            error_log[field_name].append(f'Поле не заполнено.')

    return is_valid


def validate_charset(field_names: list[str], form_data, error_log: dict[str, list[str]]) -> bool:
    is_valid = True
    for field_name in field_names:
        if field_name not in form_data:
            continue

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
