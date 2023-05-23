from django.core.mail import send_mail
from hackathon_aki import config


UNIQUE_ERRORS = {
    'email': 'Аккаунт с таким E-mail уже создан.',
    'phone_number': 'Аккаунт с таким номером телефона уже создан.',
}


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
    'description': 256
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
    'description': [
        lambda x: x.isprintable(),
    ],
}


def validate_unique(field_names: dict[str, str], form_data, model, error_log: dict[str, list[str]]) -> bool:
    is_valid = True
    for column_name, field_name in field_names.items():
        if model.objects.filter(**{column_name: form_data[field_name]}).exists():
            error_log[field_name].append(UNIQUE_ERRORS[field_name])
            is_valid = False

    return is_valid


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


def send_email_for_verify(request, user, verification_code):
    send_mail(
        "Подтверждение E-mail адреса",
        f"Перейдите по ссылке для подтверждения: {request.build_absolute_uri()[:-len(request.path)]}/email_verification/{verification_code}",
        config.EMAIL_LOGIN,
        [user.email],
        fail_silently=False,
    )


def check_user_verification(user):
    if not user.is_authenticated:
        return False

    if hasattr(user, 'client'):
        return user.client.email_verification is None
    else:
        return user.organizer.email_verification is None
