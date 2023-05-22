from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserOrganizerRegistrationForm, ProfileOrganizerRegistrationForm


def redirect_to_organizer_profile(request):
    return redirect('show_organizer_profile')


def registration(request):
    if request.method == 'POST':
        user_form = UserOrganizerRegistrationForm(request.POST)
        profile_form = ProfileOrganizerRegistrationForm(request.POST)
        print(user_form.is_valid(), user_form.errors)
        print(profile_form.is_valid(), profile_form.errors)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.username = user.email
            user.save()

            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            return HttpResponse('congrats')
        else:
            return HttpResponse('!#@$#@#')

    return render(request, 'organizers/registration.html', {'user_form': UserOrganizerRegistrationForm(),
                                                            'profile_form': ProfileOrganizerRegistrationForm()})


def show_organizer_profile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    return render(request, 'organizers/profile.html', {'email': request.user.username})
