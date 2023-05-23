import hashlib
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from main.models import PlatformAttachment
from platforms.forms import PlatformCreatingForm, PlatformFileAttachingForm
from .forms import UserOrganizerRegistrationForm, ProfileOrganizerRegistrationForm
from utils import send_email_for_verify
from form_utils import get_basic_arguments_for_html_pages


def redirect_to_organizer_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    return redirect('show_organizer_profile')


def registration(request):
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

    data = get_basic_arguments_for_html_pages(request)
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

    data['errors'] = errors
    return render(request, 'organizers/registration.html', data)


def create_platform(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    errors = {'name': [],
              'description': []}

    if request.method == 'POST':
        creating_form = PlatformCreatingForm(request.POST, request.FILES)
        attachment_form = PlatformFileAttachingForm(request.POST, request.FILES)
        if creating_form.validate(errors) and attachment_form.is_valid():
            platform = creating_form.save(commit=False)
            platform.organizer = request.user.organizer
            platform.rating = 5
            platform.save()

            for file_description in attachment_form.cleaned_data['file_field']:
                file = PlatformAttachment(platform=platform, file=file_description)
                file.save()

            return redirect('show_organizer_platforms')

    data = get_basic_arguments_for_html_pages(request)
    data['errors'] = errors
    data['creating_form'] = PlatformCreatingForm()
    data['attachment_form'] = PlatformFileAttachingForm()

    return render(request, 'platforms/create_platform.html', data)


def show_organizer_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    data = get_basic_arguments_for_html_pages(request)
    data['email'] = request.user.username

    return render(request, 'organizers/profile.html', data)


def show_organizer_platforms(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    data = get_basic_arguments_for_html_pages(request)
    data['email'] = request.user.username

    return render(request, 'organizers/profile.html', data)
