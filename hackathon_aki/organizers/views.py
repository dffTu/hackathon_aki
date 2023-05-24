from django.shortcuts import render, redirect
from main.models import PlatformAttachment
from platforms.forms import PlatformCreatingForm, PlatformFileAttachingForm
from form_utils import get_basic_arguments_for_html_pages
from login_registrate_utils import process_post_forms_requests


@process_post_forms_requests
def redirect_to_organizer_profile(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    return redirect('show_organizer_profile')


@process_post_forms_requests
def create_platform(request, data):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    errors = {'name': [],
              'description': []}

    if request.method == 'POST':
        creating_form = PlatformCreatingForm(request.POST, request.FILES)
        attachment_form = PlatformFileAttachingForm(request.POST, request.FILES)
        if creating_form.validate(errors) and attachment_form.is_valid():
            platform = creating_form.save(commit=False)
            platform.organizer = request.user.organizer
            platform.rating = 5
            platform.save()

            for file_description in attachment_form.cleaned_data['file_field']:
                file = PlatformAttachment(platform=platform, file=file_description)
                file.save()

            return redirect('show_organizer_platforms')

    data['errors'] = errors
    data['creating_form'] = PlatformCreatingForm()
    data['attachment_form'] = PlatformFileAttachingForm()

    return render(request, 'platforms/create_platform.html', data)


@process_post_forms_requests
def show_organizer_profile(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    data['email'] = request.user.username

    return render(request, 'organizers/profile.html', data)


@process_post_forms_requests
def show_organizer_platforms(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('show_client_profile')

    data['email'] = request.user.username

    return render(request, 'organizers/profile.html', data)
