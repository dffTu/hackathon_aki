from django.shortcuts import render
from .forms import ClientRegistrationForm

def registration(request):
    data = {'form': ClientRegistrationForm()}
    return render(request, 'clients/registration.html', data)

