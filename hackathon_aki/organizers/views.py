import datetime
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from main.models import PlatformAttachment
from platforms.models import Platform, FreeSlot
from platforms.forms import PlatformCreatingForm, PlatformFileAttachingForm
from .forms import FreeSlotAddingForm, UserOrganizerChangingForm, ProfileOrganizerRegistrationForm
from utils import platform_categories, DEFAULT_SLOT_PRICE, SLOTS_COUNT_FOR_PLATFORM
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
            platform.categories = request.POST['platform_category']
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

            current_date = datetime.date.today()

            for i in range(SLOTS_COUNT_FOR_PLATFORM + 1):
                new_slot = FreeSlot(platform=platform, date=current_date + datetime.timedelta(days=i),
                                    price=DEFAULT_SLOT_PRICE)
                new_slot.save()

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

    errors = {'email': [],
              'first_name': [],
              'last_name': [],
              'middle_name': [],
              'phone_number': [],
              'position': [],
              'juridical_name': [],
              'inn': []}

    if request.method == 'POST':
        user_form = UserOrganizerChangingForm(request.POST)
        profile_form = ProfileOrganizerRegistrationForm(request.POST)

        data['user_organizer_registration_form'] = user_form
        data['profile_organizer_registration_form'] = profile_form

        is_valid = user_form.validate(errors)
        is_valid = profile_form.validate(errors) and is_valid
        if is_valid:
            user = user_form.save(commit=False)
            request.user.first_name = user.first_name
            request.user.last_name = user.last_name
            request.user.save()

            user_profile = profile_form.save(commit=False)
            request.user.organizer.middle_name = user_profile.middle_name
            request.user.organizer.phone_number = user_profile.phone_number
            request.user.organizer.position = user_profile.position
            request.user.organizer.juridical_name = user_profile.juridical_name
            request.user.organizer.inn = user_profile.inn
            request.user.organizer.save()

            return redirect('show_organizer_profile')

        data['organizer_errors'] = errors
        data['has_errors'] = True
    else:
        data['user_organizer_registration_form'] = UserOrganizerChangingForm(model_to_dict(request.user))
        data['profile_organizer_registration_form'] = ProfileOrganizerRegistrationForm(model_to_dict(request.user.organizer))

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
