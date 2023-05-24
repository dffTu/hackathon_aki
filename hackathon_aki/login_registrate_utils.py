import hashlib
from platforms.search_utils import search_platforms
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from main.forms import LoginForm
from clients.forms import UserClientRegistrationForm, ProfileClientRegistrationForm
from organizers.forms import UserOrganizerRegistrationForm, ProfileOrganizerRegistrationForm
from platforms.models import Platform
from utils import send_email_for_verify
from form_utils import get_basic_arguments_for_html_pages


def login(request, data):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
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
            email_verify.verification_code = hashlib.sha512((str(email_verify.id) + "-|-" + str(datetime.now().date()) + "-|-" + str(datetime.now().time())).encode('ascii')).hexdigest()
            email_verify.save()

            user_profile = profile_form.save(commit=False)
            user_profile.email_verification = email_verify
            user_profile.save()

            send_email_for_verify(request, email_verify.email, email_verify.verification_code)
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
            email_verify.verification_code = hashlib.sha512((str(email_verify.id) + "-|-" + str(datetime.now().date()) + "-|-" + str(datetime.now().time())).encode('ascii')).hexdigest()
            email_verify.save()

            user_profile = profile_form.save(commit=False)
            user_profile.email_verification = email_verify
            user_profile.save()

            send_email_for_verify(request, email_verify.email, email_verify.verification_code)
            return render(request, 'main/email_verification_sent.html', data)

        data['user_organizer_registration_form'] = user_form
        data['profile_organizer_registration_form'] = profile_form
        data['organizer_errors'] = errors
        data['drop_localstorage'] = False

    return None


def search_platforms_by_name(request, data):
    if request.method == 'POST':
        return redirect('home')

    if request.method == 'GET':
        if request.GET['search'] == '':
            return None
        platform_names = [platform.name for platform in Platform.objects.all()]
        result_platforms = search_platforms(request.GET['search'], platform_names)
        data['platforms'] = []
        for platform_name in result_platforms:
            for platform in Platform.objects.filter(name=platform_name):
                data['platforms'].append(platform)
        data['page_id'] = 1
        return render(request, 'platforms/catalogue_page.html', data)

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
        elif request.method == "GET":
            if 'search' in request.GET:
                result = search_platforms_by_name(request, data)
                if not result is None:
                    return result
        return f(request, data, *args, **kwargs)

    return g
