from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from .forms import ClientLoginForm


def index(request):
    return render(request, 'main/index.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def login(request):
    print(request.user)
    if request.method == 'POST':
        user = auth.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return HttpResponse('congrats')
        else:
            return HttpResponse('!#@$#@#')
    else:
        return render(request, 'main/login.html', {'form': ClientLoginForm(), 'error': ''})
