from django.shortcuts import render, redirect
from django.contrib import auth
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
            data['error'] = 'Введён неправильный логин или пароль'

    return render(request, 'main/login.html', data)
