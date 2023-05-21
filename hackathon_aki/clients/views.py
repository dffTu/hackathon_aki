from django.shortcuts import render, redirect
from .forms import ClientRegistrationForm


def registration(request):
    data = {'form': ClientRegistrationForm()}
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path)
        return redirect(request.path)
    else:
        return render(request, 'clients/registration.html', data)


def show_client_profile(request):
    return render(request, 'clients/profile.html')