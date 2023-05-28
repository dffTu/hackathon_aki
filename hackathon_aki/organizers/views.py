import datetime
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from main.models import PlatformAttachment
from platforms.models import Platform
from .models import Entry
from platforms.forms import PlatformCreatingForm, PlatformFileAttachingForm
from .forms import UserOrganizerChangingForm, ProfileOrganizerRegistrationForm
from utils import platform_categories, DEFAULT_SLOT_PRICE, SLOTS_COUNT_FOR_PLATFORM
from login_registrate_utils import process_post_forms_requests
from platforms.search_utils import search_platforms


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
              'address': [],
              'agreement': []}

    if request.method == 'POST':
        is_valid = True
        if request.POST['address_text'] == '':
            errors['address'].append('Введён не корректный адрес.')
            is_valid = False

        if 'agreement' not in request.FILES:
            errors['agreement'].append('Требуется прикрепить соглашение.')
            is_valid = False

        creating_form = PlatformCreatingForm(request.POST, request.FILES)
        attachment_form = PlatformFileAttachingForm(request.POST, request.FILES)

        is_valid = creating_form.validate(errors) and is_valid
        if is_valid and attachment_form.is_valid():
            platform = creating_form.save(commit=False)
            platform.category = request.POST['platform_category']
            platform.organizer = request.user.organizer
            platform.rating = 5
            platform.address = {
                'address_text': request.POST['address_text'],
                'address_coords': [request.POST['address_latitude'], request.POST['address_longitude']],
            }
            platform.save()

            for file_description in attachment_form.cleaned_data['file_field']:
                file = PlatformAttachment(platform=platform, file=file_description)
                file.save()

            current_date = datetime.date.today()

            for i in range(SLOTS_COUNT_FOR_PLATFORM + 1):
                new_slot = Entry(client=None, platform=platform, date=current_date + datetime.timedelta(days=i),
                                 price=DEFAULT_SLOT_PRICE)
                new_slot.save()

            return redirect('show_organizer_platforms', page_id=1)

    data['errors'] = errors
    data['creating_form'] = PlatformCreatingForm()
    data['attachment_form'] = PlatformFileAttachingForm()

    data['title'] = 'Создание площадки'
    data['button_name'] = 'Создать площадку'

    return render(request, 'platforms/create_platform.html', data)


@process_post_forms_requests
def delete_entry(request, data, platform_id, client_id):
    if not request.user.is_authenticated:
        return redirect('show_platform_description', platform_id=platform_id)

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return redirect('show_platform_description', platform_id=platform_id)

    is_organizer = (hasattr(request.user, 'organizer') and platform.first().organizer == request.user.organizer)
    if not is_organizer:
        return redirect('show_platform_description', platform_id=platform_id)

    entry = Entry.objects.filter(platform_id=platform_id, client_id=client_id)
    if entry.exists():
        entry.first().delete()
    if "from_schedule" in request.POST:
        return redirect('show_organizer_schedule')
    else:
        return redirect('show_platform_description', platform_id=platform_id)


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
        data['profile_organizer_registration_form'] = ProfileOrganizerRegistrationForm(
            model_to_dict(request.user.organizer))

    return render(request, 'organizers/profile.html', data)


@process_post_forms_requests
def show_organizer_schedule(request, data):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    data['entries'] = []
    for platform in request.user.organizer.platform_set.all():
        for entry in platform.entry_set.all():
            data['entries'].append(entry)

    data['entries'].sort(key=lambda x: x.date)

    return render(request, 'organizers/profile_schedule.html', data)


@process_post_forms_requests
def redirect_to_first_page_of_organizer_platforms(request, data):
    return redirect('show_organizer_platforms', page_id=1)


@process_post_forms_requests
def show_organizer_platforms(request, data, page_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    relevant_platforms_list = Platform.objects.filter(organizer=request.user.organizer)
    data['platforms'] = []

    if 'search' in request.GET and request.GET['search'] != '':
        platform_names = [platform.name for platform in relevant_platforms_list]
        result_platforms = search_platforms(request.GET['search'], platform_names)
        relevant_platforms_list = []
        for platform_name in result_platforms:
            for platform in Platform.objects.filter(name=platform_name):
                if platform in relevant_platforms_list:
                    continue
                relevant_platforms_list.append(platform)

    number_of_platforms = len(relevant_platforms_list)
    for platform in relevant_platforms_list:
        data['platforms'].append(platform)

    data['page_id'] = page_id
    data['all_pages'] = list(range(1, (number_of_platforms + 14) // 15 + 1))

    return render(request, 'organizers/profile_platforms.html', data)


@process_post_forms_requests
def change_platform(request, data, platform_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    concurrent_platform = Platform.objects.filter(id=platform_id)
    if not concurrent_platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)
    concurrent_platform = concurrent_platform.first()

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

        data['creating_form'] = creating_form
        data['attachment_form'] = attachment_form
        data['platform_category'] = request.POST['platform_category']

        is_valid = creating_form.validate(errors) and is_valid
        if is_valid and attachment_form.is_valid():
            platform = creating_form.save(commit=False)
            concurrent_platform.name = platform.name
            concurrent_platform.short_description = platform.short_description
            concurrent_platform.description = platform.description
            if platform.agreement:
                concurrent_platform.agreement = platform.agreement
            concurrent_platform.category = request.POST['platform_category']
            concurrent_platform.address = {
                'address_text': request.POST['address_text'],
                'address_coords': [request.POST['address_latitude'], request.POST['address_longitude']],
            }
            concurrent_platform.save()

            if 'drop_old_photos' in request.POST and hasattr(concurrent_platform, 'platformattachment_set'):
                for file in concurrent_platform.platformattachment_set.all():
                    file.delete()

            for file_description in attachment_form.cleaned_data['file_field']:
                file = PlatformAttachment(platform=concurrent_platform, file=file_description)
                file.save()

            return redirect('show_platform_description', platform_id=platform_id)

        data['errors'] = errors
    else:
        data['platform_category'] = concurrent_platform.category
        data['creating_form'] = PlatformCreatingForm(model_to_dict(concurrent_platform))
        data['creating_form'].data['address'] = concurrent_platform.address['address_text']
        data['attachment_form'] = PlatformFileAttachingForm()

    data['changing'] = True
    data['title'] = 'Изменение площадки'
    data['button_name'] = 'Измененить площадку'

    return render(request, 'platforms/create_platform.html', data)
