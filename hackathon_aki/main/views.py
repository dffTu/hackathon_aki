from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import PasswordResetForm
from .models import EmailVerification, PasswordReset
from login_registrate_utils import process_post_forms_requests


@process_post_forms_requests
def index(request, data):
    return render(request, 'main/index.html', data)


@process_post_forms_requests
def logout(request, data):
    auth.logout(request)
    return redirect('home')


@process_post_forms_requests
def email_verification(request, data, verification_code):
    if request.user.is_authenticated:
        return redirect('home')

    email_verify = EmailVerification.objects.filter(verification_code=verification_code)

    if not email_verify.exists():
        data['status'] = 'Некорректный код подтверждения.'
        return render(request, 'main/email_verification.html', data)
    email_verify = email_verify.first()

    user = User(username=email_verify.email, email=email_verify.email, first_name=email_verify.first_name,
                last_name=email_verify.last_name, password=email_verify.password)
    user.save()
    data['user_fields'] = user

    if hasattr(email_verify, 'client'):
        user_data = email_verify.client
    else:
        user_data = email_verify.organizer

    user_data.user = user
    user_data.email_verification = None
    user_data.save()
    EmailVerification.objects.filter(email=email_verify.email).delete()

    auth.login(request, user)
    data['status'] = 'Почта подтверждена. Вход в аккаунт выполнен.'
    return render(request, 'main/email_verification.html', data)


@process_post_forms_requests
def reset_password(request, data, verification_code):
    if request.user.is_authenticated:
        return redirect('home')

    reset_query = PasswordReset.objects.filter(verification_code=verification_code)
    if not reset_query.exists():
        data['error_status'] = 'Некорректный код подтверждения.'
        return render(request, 'main/forget_password_fowm.html', data)
    reset_query = reset_query.first()

    user = User.objects.filter(username=reset_query.email)
    if not user.exists():
        data['error_status'] = 'Пользователь был удалён.'
        return render(request, 'main/forget_password_fowm.html', data)
    user = user.first()

    errors = {'password': [],
              'repeat_password': []}

    if request.method == 'POST':
        is_valid = True
        if request.POST['password'] != request.POST['repeat_password']:
            errors['repeat_password'].append('Пароли не совпадают')
            is_valid = False

        form = PasswordResetForm(request.POST)

        is_valid = form.validate(errors) and is_valid
        if is_valid:
            reset_query.delete()

            user.set_password(request.POST['password'])
            user.save()

            auth.login(request, user)

            return redirect('show_client_profile')

        data['errors'] = errors
        data['form'] = form
    else:
        data['form'] = PasswordResetForm()

    return render(request, 'main/forget_password_fowm.html', data)
