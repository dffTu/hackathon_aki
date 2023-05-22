from django.shortcuts import render, redirect
from django.contrib import auth
from main.models import PlatformAttachment
from platforms.forms import PlatformCreatingForm, PlatformFileAttachingForm
from .forms import UserOrganizerRegistrationForm, ProfileOrganizerRegistrationForm
from form_utils import get_basic_arguments_for_html_pages


def redirect_to_organizer_profile(request):
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

    if request.method == 'POST':
        is_valid = True
        if request.POST['password'] != request.POST['repeat_password']:
            errors['repeat_password'].append('Пароли не совпадают')
            is_valid = False

        user_form = UserOrganizerRegistrationForm(request.POST)
        profile_form = ProfileOrganizerRegistrationForm(request.POST)

        is_valid = user_form.validate(errors) and is_valid
        is_valid = profile_form.validate(errors) and is_valid
        if is_valid:
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.username = user.email
            user.save()

            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()

            auth.login(request, user)
            return redirect(request.path)

    data = get_basic_arguments_for_html_pages()
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

    data = get_basic_arguments_for_html_pages()
    data['errors'] = errors
    data['creating_form'] = PlatformCreatingForm()
    data['attachment_form'] = PlatformFileAttachingForm()

    return render(request, 'platforms/create_platform.html', data)


def show_organizer_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    data = get_basic_arguments_for_html_pages()
    data['email'] = request.user.username

    return render(request, 'organizers/profile.html', data)


def show_organizer_platforms(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    data = get_basic_arguments_for_html_pages()
    data['email'] = request.user.username

    return render(request, 'organizers/profile.html', data)
