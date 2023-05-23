import hashlib
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import UserClientRegistrationForm, ProfileClientRegistrationForm
from utils import send_email_for_verify
from form_utils import get_basic_arguments_for_html_pages


def redirect_to_client_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        return redirect('show_organizer_profile')

    return redirect('show_client_profile')


def registration(request):
    if request.user.is_authenticated:
        return redirect('show_client_profile')

    errors = {'email': [],
              'password': [],
              'repeat_password': [],
              'first_name': [],
              'last_name': [],
              'middle_name': [],
              'phone_number': []}

    data = get_basic_arguments_for_html_pages(request)
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

    data['user_form'] = UserClientRegistrationForm()
    data['profile_form'] = ProfileClientRegistrationForm()
    data['errors'] = errors
    return render(request, 'clients/registration.html', data)


def show_client_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        return redirect('show_organizer_profile')

    data = get_basic_arguments_for_html_pages(request)
    data['email'] = request.user.username

    return render(request, 'clients/profile.html', data)
