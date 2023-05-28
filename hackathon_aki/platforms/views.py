import pandas as pd
import datetime
from django.http import FileResponse
from django.shortcuts import render, redirect
from .models import Platform
from organizers.models import Entry
from main.models import CommentAttachment
from .forms import CommentFileAttachingForm, CommentLeavingForm, CalendarImportingForm
from login_registrate_utils import process_post_forms_requests, show_catalogue_page
from calendar_utils import Month, build_calendar


@process_post_forms_requests
def redirect_to_first_page(request, data):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


@process_post_forms_requests
def show_page(request, data, page_id):            # Shows catalogue page
    relevant_platforms_list = Platform.objects.filter(verified=True)
    data['catalogue_type'] = 'show_page'
    return show_catalogue_page(request, data, page_id, relevant_platforms_list)


@process_post_forms_requests
def show_platform_description(request, data, platform_id):
    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)
    is_organizer = (hasattr(request.user, 'organizer') and platform.first().organizer == request.user.organizer)
    if not platform.first().verified and not request.user.is_staff and not is_organizer:
        return render(request, 'platforms/platform_not_found.html', data)

    platform = platform.first()
    data['platform'] = platform
    data['months'] = build_calendar(platform_id)
    data['comment_leaving_form'] = CommentLeavingForm()
    data['attachment_form'] = CommentFileAttachingForm()
    data['calendar_importing_form'] = CalendarImportingForm()

    return render(request, 'platforms/platform_description.html', data)


@process_post_forms_requests
def leave_comment(request, data, platform_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'client'):
        return redirect('show_platform_description', platform_id=platform_id)

    data['platform_id'] = platform_id

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists() or not platform.first().verified:
        return render(request, 'platforms/platform_not_found.html', data)
    platform = platform.first()

    errors = {'text': [],
              'rating': []}

    if request.method == 'POST':
        comment_form = CommentLeavingForm(request.POST)
        attachment_form = CommentFileAttachingForm(request.POST, request.FILES)
        if comment_form.validate(errors) and attachment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.client = request.user.client
            comment.platform = platform
            comment.save()
            platform.rating = (platform.rating * (len(platform.comment_set.all()) - 1) + comment.rating) / len(platform.comment_set.all())
            platform.save()

            for file_description in attachment_form.cleaned_data['file_field']:
                file = CommentAttachment(comment=comment, file=file_description)
                file.save()

            return redirect('show_platform_description', platform_id=platform_id)

    data['errors'] = errors
    data['comment_form'] = CommentLeavingForm()
    data['attachment_form'] = CommentFileAttachingForm()

    return render(request, 'platforms/leave_comment.html', data)


@process_post_forms_requests
def delete_platform(request, data, platform_id):
    if not request.user.is_authenticated:
        return redirect('show_platform_description', platform_id=platform_id)

    platform = Platform.objects.filter(id=platform_id)
    is_organizer = (hasattr(request.user, 'organizer') and platform.first().organizer == request.user.organizer)

    if request.user.is_staff:
        if not platform.exists():
            return render(request, 'platforms/platform_not_found.html', data)
        platform.first().delete()
        return redirect('show_unverified_page', page_id=1)
    elif is_organizer:
        if not platform.exists():
            return render(request, 'platforms/platform_not_found.html', data)
        platform.first().delete()
        return redirect('show_organizer_platforms', page_id=1)
    else:
        return redirect('show_platform_description', platform_id=platform_id)


@process_post_forms_requests
def verify_platform(request, data, platform_id):
    if not request.user.is_authenticated:
        return redirect('show_platform_description', platform_id=platform_id)

    if request.user.is_staff:
        platform = Platform.objects.filter(id=platform_id)
        if not platform.exists():
            return render(request, 'platforms/platform_not_found.html', data)

        this_platform = platform.first()
        this_platform.verified = True
        this_platform.save()
        return redirect('show_unverified_page', page_id=1)
    else:
        return redirect('show_platform_description', platform_id=platform_id)


@process_post_forms_requests
def unverify_platform(request, data, platform_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('show_platform_description', platform_id=platform_id)

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)

    this_platform = platform.first()
    this_platform.verified = False
    this_platform.save()
    return redirect('show_page', page_id=1)


@process_post_forms_requests
def download_agreement(request, data, platform_id):
    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)

    return FileResponse(platform.first().agreement, as_attachment=True)


@process_post_forms_requests
def update_platform_schedule(request, data, platform_id):
    if not request.user.is_authenticated or request.method != 'POST' or request.user.is_staff:
        return redirect('show_platform_description', platform_id=platform_id)

    platform = Platform.objects.filter(id=platform_id)
    is_organizer = (hasattr(request.user, 'organizer') and platform.first().organizer == request.user.organizer)

    if not is_organizer:
        return redirect('show_platform_description', platform_id=platform_id)

    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)

    form = CalendarImportingForm(request.POST, request.FILES)
    form.is_valid()

    if form.cleaned_data['file_field']:
        calendar_data = pd.read_excel(form.cleaned_data['file_field'])
        for i in range(calendar_data.shape[0]):
            date = calendar_data[calendar_data.columns[0]][i].to_pydatetime()
            price = int(calendar_data[calendar_data.columns[1]][i])
            entry = Entry(platform_id=platform_id, date=date, price=price)
            entry.save()

    return redirect('show_platform_description', platform_id=platform_id)
