from django.shortcuts import render
from .forms import ClientLoginForm


def index(request):
    return render(request, 'main/index.html')


def login(request):
    data = {
        'form': ClientLoginForm()
    }
    return render(request, 'main/login.html', data)
