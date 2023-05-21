from django.shortcuts import render, redirect
from .forms import OrganizerRegistrationForm


def registration(request):
    data = {'form': OrganizerRegistrationForm()}
    if request.method == 'POST':
        form = OrganizerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path)
        return redirect(request.path)
    else:
        return render(request, 'clients/registration.html', data)


def redirect_to_organizer_profile(request):
    return redirect('/organizer/profile')


def show_organizer_profile(request):
    return render(request, 'organizers/profile.html')
