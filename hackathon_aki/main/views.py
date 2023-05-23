from django.shortcuts import render, redirect
from django.contrib import auth
from .models import EmailVerification
from utils import check_user_verification
from form_utils import get_basic_arguments_for_html_pages


def index(request):
    data = get_basic_arguments_for_html_pages()
    return render(request, 'main/index.html', data)


def logout(request):
    auth.logout(request)
    return redirect('home')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    data = get_basic_arguments_for_html_pages()
    if request.method == 'POST':
        user = auth.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect(request.path)
        else:
            data['error_message'] = 'Введён неправильный логин или пароль'

    return render(request, 'main/login.html', data)


def email_verification(request, verification_code):
    data = get_basic_arguments_for_html_pages()
    if not request.user.is_authenticated:
        data['status'] = 'Для подтверждения адреса электронной почты требуется войти в аккаунт.'
        return render(request, 'main/email_verification.html', data)

    if hasattr(request.user, 'client'):
        user_data = request.user.client
    else:
        user_data = request.user.organizer

    if user_data.email_verification is None:
        return redirect('home')

    if user_data.email_verification.id != verification_code:
        data['status'] = 'Некорректный код подтверждения.'
        return render(request, 'main/email_verification.html', data)

    user_data.email_verification = None
    user_data.save()
    EmailVerification.objects.filter(email=request.user.email).delete()

    data['status'] = 'Почта подтверждена.'
    return render(request, 'main/email_verification.html', data)
