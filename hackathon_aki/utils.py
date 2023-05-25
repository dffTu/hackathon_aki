from django.core.mail import send_mail
from hackathon_aki import config

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

platform_categories = {
    'platform-type': {
        'ru': 'Тип площадки',
        'filters': [
            ('film-studio', 'Киностудия'),
            ('gallery', 'Галерея'),
            ('publishing-house', 'Издательство'),
            ('book-shop', 'Книжный магазин'),
            ('design-studio', 'Дизайн студия'),
            ('creative-space', 'Креативное пространство'),
            ('cinema-theater', 'Кинотеатр'),
            ('sound-recording-studio', 'Звукозаписывающая студия'),
            ('AR-VR-studio', 'AR-VR-студия')
        ]
    },
    'price': {
        'ru': 'Цена',
        'filters': [
            ('big-price', 'Большая цена'),
            ('medium-price', 'Средняя цена'),
            ('small-price', 'Малая цена')
        ]
    },
}


def validate_length(field_names: list[str], required_fields: list[str], form_data,
                    error_log: dict[str, list[str]]) -> bool:
    is_valid = True
    for field_name in field_names:
        if field_name not in form_data:
            continue

        if len(form_data[field_name]) > MAX_LENGTH[field_name]:
            error_log[field_name].append(f'Превышено максимальное число символов {MAX_LENGTH[field_name]}')
            is_valid = False

    for field_name in required_fields:
        if field_name not in form_data or len(form_data[field_name]) == 0:
            error_log[field_name].append('Поле не заполнено.')
            is_valid = False

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
