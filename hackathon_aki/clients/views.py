from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserClientRegistrationForm, ProfileClientRegistrationForm


def redirect_to_client_profile(request):
    return redirect('show_client_profile')


def registration(request):
    if request.method == 'POST':
        user_form = UserClientRegistrationForm(request.POST)
        profile_form = ProfileClientRegistrationForm(request.POST)
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

    return render(request, 'clients/registration.html', {'user_form': UserClientRegistrationForm(),
                                                         'profile_form': ProfileClientRegistrationForm()})


def show_client_profile(request):
    return render(request, 'clients/profile.html')
