from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import EmailVerification
from form_utils import get_basic_arguments_for_html_pages


def index(request):
    data = get_basic_arguments_for_html_pages(request)
    return render(request, 'main/index.html', data)


def logout(request):
    auth.logout(request)
    return redirect('home')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    data = get_basic_arguments_for_html_pages(request)
    if request.method == 'POST':
        user = auth.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect(request.path)
        else:
            data['error_message'] = 'Введён неправильный логин или пароль'

    return render(request, 'main/login.html', data)


def email_verification(request, verification_code):
    if request.user.is_authenticated:
        return redirect('home')

    email_verify = EmailVerification.objects.filter(verification_code=verification_code)

    data = get_basic_arguments_for_html_pages(request)
    if not email_verify.exists():
        data['status'] = 'Некорректный код подтверждения.'
        return render(request, 'main/email_verification.html', data)
    email_verify = email_verify.first()

    user = User(username=email_verify.email, email=email_verify.email, first_name=email_verify.first_name,
                last_name=email_verify.last_name, password=email_verify.password)
    user.save()

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
