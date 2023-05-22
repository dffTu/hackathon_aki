from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import UserClientRegistrationForm, ProfileClientRegistrationForm
from form_utils import get_basic_arguments_for_html_pages


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
            return redirect(request.path)

    data = get_basic_arguments_for_html_pages()
    data['user_form'] = UserClientRegistrationForm()
    data['profile_form'] = ProfileClientRegistrationForm()
    data['errors'] = errors

    return render(request, 'clients/registration.html', data)


def show_client_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        return redirect('show_organizer_profile')

    data = get_basic_arguments_for_html_pages()
    data['email'] = request.user.username

    return render(request, 'clients/profile.html', data)
