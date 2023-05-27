import hashlib
import datetime
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from main.forms import LoginForm
from clients.forms import UserClientRegistrationForm, ProfileClientRegistrationForm
from organizers.forms import UserOrganizerRegistrationForm, ProfileOrganizerRegistrationForm
from main.models import PasswordReset
from organizers.models import Entry
from platforms.search_utils import search_platforms
from platforms.models import Platform
from platforms.forms import CommentLeavingForm, CommentFileAttachingForm
from utils import send_email_for_verify, send_email_for_reset_password
from utils import platform_categories
from form_utils import get_basic_arguments_for_html_pages


def login(request, data):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        if request.POST['__is_password_reset'] == 'Y':
            data['email'] = request.POST['email']

            if not User.objects.filter(username=request.POST['email']).exists():
                data['error'] = f"Аккаунт в почтой {request.POST['email']} не зарегистрирован."
            else:
                reset_query = PasswordReset(email=request.POST['email'])
                reset_query.save()
                reset_query.verification_code = hashlib.sha512((str(reset_query.id) + "-|-" + str(datetime.datetime.now().date()) + "-|-" + str(datetime.datetime.now().time())).encode('ascii')).hexdigest()
                reset_query.save()

                try:
                    send_email_for_reset_password(request, reset_query.email, reset_query.verification_code)
                except:
                    data['error'] = f"Введён некорректный E-mail."
                    reset_query.delete()

            return render(request, 'main/forget_password.html', data)

        user = auth.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect(request.path)
        else:
            data['error'] = 'Введён неправильный логин или пароль'

        data['login_form'] = LoginForm(request.POST)
        data['drop_localstorage'] = False

    return None


def client_registration(request, data):
    if request.user.is_authenticated:
        return redirect('show_client_profile')

    errors = {'email': [],
              'password': [],
              'repeat_password': [],
              'first_name': [],
              'last_name': [],
              'middle_name': [],
              'phone_number': []}

    if request.method == 'POST':
        is_valid = True
        if request.POST['password'] != request.POST['repeat_password']:
            errors['repeat_password'].append('Пароли не совпадают')
            is_valid = False

        if User.objects.filter(username=request.POST['email']).exists():
            errors['email'].append('Аккаунт с таким E-mail уже создан.')
            is_valid = False

        user_form = UserClientRegistrationForm(request.POST)
        profile_form = ProfileClientRegistrationForm(request.POST)

        is_valid = user_form.validate(errors) and is_valid
        is_valid = profile_form.validate(errors) and is_valid
        if is_valid:
            email_verify = user_form.save(commit=False)
            email_verify.password = auth.hashers.make_password(email_verify.password)
            email_verify.save()
            email_verify.verification_code = hashlib.sha512((str(email_verify.id) + "-|-" + str(datetime.datetime.now().date()) + "-|-" + str(datetime.datetime.now().time())).encode('ascii')).hexdigest()
            email_verify.save()

            user_profile = profile_form.save(commit=False)
            user_profile.email_verification = email_verify
            user_profile.save()

            try:
                send_email_for_verify(request, email_verify.email, email_verify.verification_code)
            except:
                errors['email'].append('Введён некорректный E-mail.')
                email_verify.delete()
                user_profile.delete()

            return render(request, 'main/email_verification_sent.html', data)

        data['user_client_registration_form'] = user_form
        data['profile_client_registration_form'] = profile_form
        data['client_errors'] = errors
        data['drop_localstorage'] = False

    return None


def organizer_registration(request, data):
    if request.user.is_authenticated:
        return redirect('show_organizer_profile')

    errors = {'email': [],
              'password': [],
              'repeat_password': [],
              'first_name': [],
              'last_name': [],
              'middle_name': [],
              'phone_number': [],
              'position': [],
              'juridical_name': [],
              'inn': []}

    if request.method == 'POST':
        is_valid = True
        if request.POST['password'] != request.POST['repeat_password']:
            errors['repeat_password'].append('Пароли не совпадают')
            is_valid = False

        if User.objects.filter(username=request.POST['email']).exists():
            errors['email'].append('Аккаунт с таким E-mail уже создан.')
            is_valid = False

        user_form = UserOrganizerRegistrationForm(request.POST)
        profile_form = ProfileOrganizerRegistrationForm(request.POST)

        is_valid = user_form.validate(errors) and is_valid
        is_valid = profile_form.validate(errors) and is_valid
        if is_valid:
            email_verify = user_form.save(commit=False)
            email_verify.password = auth.hashers.make_password(email_verify.password)
            email_verify.save()
            email_verify.verification_code = hashlib.sha512((str(email_verify.id) + "-|-" + str(datetime.datetime.now().date()) + "-|-" + str(datetime.datetime.now().time())).encode('ascii')).hexdigest()
            email_verify.save()

            user_profile = profile_form.save(commit=False)
            user_profile.email_verification = email_verify
            user_profile.save()

            try:
                send_email_for_verify(request, email_verify.email, email_verify.verification_code)
            except:
                errors['email'].append('Введён некорректный E-mail.')
                email_verify.delete()
                user_profile.delete()

            return render(request, 'main/email_verification_sent.html', data)

        data['user_organizer_registration_form'] = user_form
        data['profile_organizer_registration_form'] = profile_form
        data['organizer_errors'] = errors
        data['drop_localstorage'] = False

    return None


def save_search_request(request, data):
    if 'search' in request.GET and request.GET['search'] != '':
        data['filters']['search'] = request.GET['search']


def save_filters_request(request, data):
    for category in platform_categories:
        for category_filter in platform_categories[category]['filters']:
            if category_filter in request.GET:
                print(category_filter)
                data['filters'][category_filter] = 'on'


def save_prices_request(request, data):
    if 'min_price' in request.GET:
        data['filters']['min_price'] = request.GET['min_price']
    if 'max_price' in request.GET:
        data['filters']['max_price'] = request.GET['max_price']


def save_get_request(request, data):
    save_search_request(request, data)
    save_filters_request(request, data)
    save_prices_request(request, data)


def calendar_entry_request(request, data):
    print(request.POST)
    if not request.user.is_authenticated:
        return redirect('show_page', page_id=1)
    if hasattr(request.user, 'organizer'):
        return redirect(request.path)
    platform_id = int(request.POST['__platform_id'])
    day = int(request.POST['__day'])
    month = int(request.POST['__month'])
    year = int(request.POST['__year'])
    date = datetime.date(year, month, day)
    entry = Entry(client=request.user.client, platform_id=platform_id, date=date)
    entry.save()


def show_catalogue_page(request, data, page_id, relevant_platforms_list):
    if 'search' in request.GET and request.GET['search'] != '':
        platform_names = [platform.name for platform in relevant_platforms_list]
        result_platforms = search_platforms(request.GET['search'], platform_names)
        relevant_platforms_list = []
        for platform_name in result_platforms:
            for platform in Platform.objects.filter(name=platform_name):
                if platform in relevant_platforms_list:
                    continue
                relevant_platforms_list.append(platform)

    minimal_price = 0
    maximal_price = 1000000
    if 'min_price' in request.GET and request.GET['min_price'].isdecimal():
        minimal_price = int(request.GET['min_price'])
    if 'max_price' in request.GET and request.GET['max_price'].isdecimal():
        maximal_price = int(request.GET['max_price'])

    data['platforms'] = []

    relevant_platforms_list_temp = [platform for platform in relevant_platforms_list]
    relevant_platforms_list = []

    for platform in relevant_platforms_list_temp:
        should_add = False
        for slot in platform.freeslot_set.all():
            if datetime.date.today() > slot.date:
                continue
            if minimal_price <= slot.price <= maximal_price:
                should_add = True
                break
        if should_add:
            relevant_platforms_list.append(platform)

    filters = []
    selected_category = {}
    for category_type in platform_categories:
        selected_category[category_type] = False
        for category_filter in platform_categories[category_type]['filters']:
            if category_filter in request.GET:
                filters.append(category_filter)
                selected_category[category_type] = True

    data['platforms'] = []

    number_of_platforms = 0
    if not filters:
        number_of_platforms = len(relevant_platforms_list)
        for platform in relevant_platforms_list:
            data['platforms'].append(platform)
    else:
        for platform in relevant_platforms_list:
            should_add = True
            for category_type in platform_categories:
                if not selected_category[category_type]:
                    continue
                found_tag = False
                for category_filter in platform_categories[category_type]['filters']:
                    if category_filter in platform.categories.split(';') and category_filter in filters:
                        found_tag = True
                        break
                if not found_tag:
                    should_add = False
                    break
            if should_add:
                data['platforms'].append(platform)
                number_of_platforms += 1

    data['page_id'] = page_id
    data['all_pages'] = list(range(1, (number_of_platforms + 14) // 15 + 1))

    return render(request, 'platforms/catalogue_page.html', data)


def leave_comment(request, data):
    if 'platform_id' not in request.POST:
        return redirect('show_page', page_id=1)
    platform = Platform.objects.filter(id=request.POST['platform_id'])
    if not platform.exists():
        return redirect('show_page', page_id=1)
    platform = platform.first()
    if not request.user.is_authenticated or not hasattr(request.user, 'client'):
        return redirect('show_platform_description', platform_id=platform.id)

    errors = {
        'text': [],
        'rating': []
    }

    if request.method == 'POST':
        is_valid = True
        platform_id = int(request.POST['platform_id'])
        comment_form = CommentLeavingForm(request.POST)
        attachment_form = CommentFileAttachingForm(request.POST, request.FILES)
        if comment_form.validate(errors) and attachment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.client = request.user.client
            comment.platform = platform
            comment.save()
            platform.rating = (platform.rating * (len(platform.comment_set.all()) - 1) + comment.rating) / len(platform.comment_set.all())
            platform.save()
        else:
            is_valid = False

        data['errors'] = errors
        data['comment_form'] = CommentLeavingForm()
        data['attachment_form'] = CommentFileAttachingForm()
        data['drop_localstorage'] = False

        if is_valid:
            return redirect('show_platform_description', platform_id=platform_id)

    return None


def process_post_forms_requests(f):
    def g(request, *args, **kwargs):
        data = get_basic_arguments_for_html_pages(request)
        if request.method == "POST":
            if '__login_form' in request.POST:
                result = login(request, data)
                if not result is None:
                    return result
            if '__client_register' in request.POST:
                result = client_registration(request, data)
                if not result is None:
                    return result
            if '__organizer_register' in request.POST:
                result = organizer_registration(request, data)
                if not result is None:
                    return result
            if '__calendar_entry_request' in request.POST:
                result = calendar_entry_request(request, data)
                if not result is None:
                    return result
            if '__comment_leaving_form' in request.POST:
                result = leave_comment(request, data)
                if not result is None:
                    return result
        elif request.method == "GET":
            if "__search_form" in request.GET or "__filter_form" in request.GET:
                result = save_get_request(request, data)
                if not result is None:
                    return result

        return f(request, data, *args, **kwargs)

    return g
