from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from .forms import UserClientChangingForm, ProfileClientRegistrationForm
from login_registrate_utils import process_post_forms_requests


@process_post_forms_requests
def redirect_to_client_profile(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        if not hasattr(request.user, 'organizer'):
            return redirect('home')
        return redirect('show_organizer_profile')

    return redirect('show_client_profile')


@process_post_forms_requests
def show_client_profile(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        if not hasattr(request.user, 'organizer'):
            return redirect('home')
        return redirect('show_organizer_profile')

    errors = {'email': [],
              'first_name': [],
              'last_name': [],
              'middle_name': [],
              'phone_number': []}

    if request.method == 'POST':
        user_form = UserClientChangingForm(request.POST)
        profile_form = ProfileClientRegistrationForm(request.POST)

        data['user_client_registration_form'] = user_form
        data['profile_client_registration_form'] = profile_form

        is_valid = user_form.validate(errors)
        is_valid = profile_form.validate(errors) and is_valid
        if is_valid:
            user = user_form.save(commit=False)
            request.user.first_name = user.first_name
            request.user.last_name = user.last_name
            request.user.save()

            user_profile = profile_form.save(commit=False)
            request.user.client.middle_name = user_profile.middle_name
            request.user.client.phone_number = user_profile.phone_number
            request.user.client.save()

            return redirect('show_client_profile')

        data['client_errors'] = errors
        data['has_errors'] = True
    else:
        data['user_client_registration_form'] = UserClientChangingForm(model_to_dict(request.user))
        data['profile_client_registration_form'] = ProfileClientRegistrationForm(model_to_dict(request.user.client))

    return render(request, 'clients/profile.html', data)


@process_post_forms_requests
def show_client_entries(request, data):
    if not request.user.is_authenticated or not hasattr(request.user, 'client'):
        return redirect('home')

    data['entries'] = list(request.user.client.entry_set.all())
    data['entries'].sort(key=lambda x: x.date)

    return render(request, 'clients/profile_entries.html', data)
