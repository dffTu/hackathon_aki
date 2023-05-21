from django.shortcuts import render, redirect
from .forms import UserClientRegistrationForm, ProfileClientRegistrationForm


def registration(request):
    if request.method == 'POST':
        user_form = UserClientRegistrationForm(request.POST)
        profile_form = ProfileClientRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

        return redirect(request.path)

    return render(request, 'clients/registration.html', {'user_form': UserClientRegistrationForm(),
                                                         'profile_form': ProfileClientRegistrationForm()})


def redirect_to_client_profile(request):
    return redirect('/organizer/profile')


def show_client_profile(request):
    return render(request, 'clients/profile.html')
