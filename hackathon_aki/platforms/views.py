from django.shortcuts import render, redirect
from .models import Platform, Comment
from main.models import CommentAttachment
from .forms import CommentFileAttachingForm, CommentLeavingForm
from login_registrate_utils import process_post_forms_requests
from utils import Day
import datetime

from random import randint


@process_post_forms_requests
def redirect_to_first_page(request, data):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


@process_post_forms_requests
def show_page(request, data, page_id):            # Shows catalogue page
    platforms = Platform.objects.all()

    data['page_id'] = page_id
    data['platforms'] = platforms

    return render(request, 'platforms/catalogue_page.html', data)


@process_post_forms_requests
def show_platform_description(request, data, platform_id):
    data['platform_id'] = platform_id

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)
    platform = platform.first()

    data['comments'] = Comment.objects.filter(platform=platform)

    return render(request, 'platforms/platform_description.html', data)


@process_post_forms_requests
def leave_comment(request, data, platform_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'client'):
        return redirect('show_platform_description', platform_id=platform_id)

    data['platform_id'] = platform_id

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
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

            for file_description in attachment_form.cleaned_data['file_field']:
                file = CommentAttachment(comment=comment, file=file_description)
                file.save()

            return redirect('show_platform_description', platform_id=platform_id)

    data['errors'] = errors
    data['comment_form'] = CommentLeavingForm()
    data['attachment_form'] = CommentFileAttachingForm()

    return render(request, 'platforms/leave_comment.html', data)


@process_post_forms_requests
def calendar(request, data):
    today = datetime.date.today()
    calendar = []

    for week in range(5):
        week_table = []
        for weekday in range(7):
            delta = weekday - today.weekday() + week * 7
            if delta < 0:
                state = 'previous'
            elif delta == 0:
                state = 'today'
            else:
                state = 'future'
            tmp_date = datetime.date.today() + datetime.timedelta(delta)
            week_table.append(Day(tmp_date, state))

        for _ in range(2):
            week_table[randint(0, 6)].state = "booked"
        calendar.append(week_table)

    data['calendar'] = calendar

    return render(request, 'platforms/calendar.html', data)
