from django.shortcuts import render, redirect
from django.contrib import auth
from utils import send_email_for_verify
from .forms import UserClientRegistrationForm, ProfileClientRegistrationForm


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
        is_valid = True
        if request.POST['password'] != request.POST['repeat_password']:
            errors['repeat_password'].append('Пароли не совпадают')
            is_valid = False

        user_form = UserClientRegistrationForm(request.POST)
        profile_form = ProfileClientRegistrationForm(request.POST)

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
            send_email_for_verify(user)
            return redirect(request.path)

    return render(request, 'clients/registration.html', {'user_form': UserClientRegistrationForm(),
                                                         'profile_form': ProfileClientRegistrationForm(),
                                                         'errors': errors})


def show_client_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        return redirect('show_organizer_profile')

    return render(request, 'clients/profile.html', {'email': request.user.username})
