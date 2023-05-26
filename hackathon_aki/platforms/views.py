from django.shortcuts import render, redirect
from .models import Platform, Comment
from main.models import CommentAttachment
from .forms import CommentFileAttachingForm, CommentLeavingForm
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
    if not request.user.is_staff and not is_organizer:
        return render(request, 'platforms/platform_not_found.html', data)

    data['platform'] = platform.first()
    data['comments'] = Comment.objects.filter(platform_id=platform_id)
    data['comments_amount'] = len(data['comments'])
    data['months'] = build_calendar(platform_id)

    return render(request, 'platforms/platform_description.html', data)


@process_post_forms_requests
def leave_comment(request, data, platform_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'client'):
        return redirect('show_platform_description', platform_id=platform_id)

    data['platform_id'] = platform_id

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists() or not platform.verified:
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
def delete_platform(request, data, platform_id):
    if not request.user.is_authenticated:
        return redirect('show_platform_description', platform_id=platform_id)

    if request.user.is_staff:
        platform = Platform.objects.filter(id=platform_id)
        if not platform.exists():
            return render(request, 'platforms/platform_not_found.html', data)
        platform.first().delete()
        return redirect('show_unverified_page', page_id=1)
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
