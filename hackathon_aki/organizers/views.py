from django.shortcuts import render, redirect
from main.models import PlatformAttachment
from platforms.models import Platform
from platforms.forms import PlatformCreatingForm, PlatformFileAttachingForm
from .forms import FreeSlotAddingForm
from login_registrate_utils import process_post_forms_requests


@process_post_forms_requests
def redirect_to_organizer_profile(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        if not hasattr(request.user, 'client'):
            return redirect('home')
        return redirect('show_client_profile')

    return redirect('show_organizer_profile')


@process_post_forms_requests
def create_platform(request, data):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    errors = {'name': [],
              'short_description': [],
              'description': [],
              'categories': [],
              'address': []}

    if request.method == 'POST':
        is_valid = True
        if request.POST['address_text'] == '':
            errors['address'].append('Введён не корректный адрес.')
            is_valid = False

        creating_form = PlatformCreatingForm(request.POST, request.FILES)
        attachment_form = PlatformFileAttachingForm(request.POST, request.FILES)

        is_valid = creating_form.validate(errors) and is_valid
        if is_valid and attachment_form.is_valid():
            platform = creating_form.save(commit=False)
            platform.organizer = request.user.organizer
            platform.rating = 5
            platform.address = {
                'address_text':  request.POST['address_text'],
                'address_coords': [request.POST['address_latitude'], request.POST['address_longitude']],
            }
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
def add_free_slot(request, data, platform_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)
    platform = platform.first()

    errors = {'date': [],
              'price': []}

    if request.method == 'POST':
        form = FreeSlotAddingForm(request.POST)
        if form.is_valid():
            free_slot = form.save(commit=False)
            free_slot.platform = platform
            free_slot.save()

            return redirect('show_organizer_platforms')

    data['form'] = FreeSlotAddingForm()
    data['errors'] = errors

    return render(request, 'organizers/add_free_slot.html', data)


@process_post_forms_requests
def show_organizer_profile(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        if not hasattr(request.user, 'client'):
            return redirect('home')
        return redirect('show_client_profile')

    data['profile'] = request.user

    return render(request, 'organizers/profile.html', data)


@process_post_forms_requests
def show_organizer_schedule(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('home')

    data['email'] = request.user.username

    return render(request, 'organizers/profile_schedule.html', data)


@process_post_forms_requests
def show_organizer_platforms(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'organizer'):
        return redirect('home')

    data['email'] = request.user.username

    return render(request, 'organizers/profile_platforms.html', data)

