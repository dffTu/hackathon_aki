from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Client
from .forms import UserClientRegistrationForm, ProfileClientRegistrationForm
from utils import validate_unique, validate_length, validate_charset


def redirect_to_client_profile(request):
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

    if request.method == 'POST':
        user_form = UserClientRegistrationForm(request.POST)
        profile_form = ProfileClientRegistrationForm(request.POST)

        is_valid = True
        if request.POST['password'] != request.POST['repeat_password']:
            errors['repeat_password'].append('Пароли не совпадают')
            is_valid = False

        is_valid = validate_unique(UserClientRegistrationForm.unique_fields, request.POST, User, errors) and is_valid
        is_valid = validate_unique(ProfileClientRegistrationForm.unique_fields, request.POST, Client, errors) and is_valid

        is_valid = validate_length(UserClientRegistrationForm.length_validation_fields, request.POST, errors) and is_valid
        is_valid = validate_length(ProfileClientRegistrationForm.length_validation_fields, request.POST, errors) and is_valid

        is_valid = validate_charset(UserClientRegistrationForm.charset_validation_fields, request.POST, errors) and is_valid
        is_valid = validate_charset(ProfileClientRegistrationForm.charset_validation_fields, request.POST, errors) and is_valid

        if is_valid:
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.username = user.email
            user.save()

            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            return redirect(request.path)

    return render(request, 'clients/registration.html', {'user_form': UserClientRegistrationForm(),
                                                         'profile_form': ProfileClientRegistrationForm(),
                                                         'errors': errors})


def show_client_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        return redirect('show_organizer_profile')

    return render(request, 'clients/profile.html')
