from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import ClientLoginForm


def index(request):
    auth.logout(request)
    print(request.user)
    return render(request, 'main/index.html')


def login(request):
    print(request.user)
    if request.method == 'POST':
        user = auth.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
        else:
            return render(request, 'main/login.html', {'form': ClientLoginForm(), 'error': 'ERROR'})
    else:
        return render(request, 'main/login.html', {'form': ClientLoginForm(), 'error': ''})
