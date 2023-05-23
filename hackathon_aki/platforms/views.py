from django.shortcuts import render, redirect
from .models import Platform, Comment
from main.models import CommentAttachment
from .forms import CommentFileAttachingForm, CommentLeavingForm
from form_utils import get_basic_arguments_for_html_pages


def redirect_to_first_page(request):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


def show_page(request, page_id):            # Shows catalogue page
    platforms = Platform.objects.all()

    data = get_basic_arguments_for_html_pages(request.user)
    data['page_id'] = page_id
    data['platforms'] = platforms

    return render(request, 'platforms/catalogue_page.html', data)


def show_platform_description(request, platform_id):
    data = get_basic_arguments_for_html_pages(request.user)
    data['platform_id'] = platform_id

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)
    platform = platform.first()

    data['comments'] = Comment.objects.filter(platform=platform)

    return render(request, 'platforms/platform_description.html', data)


def leave_comment(request, platform_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'client'):
        return redirect('show_platform_description', platform_id=platform_id)

    data = get_basic_arguments_for_html_pages(request.user)
    data['platform_id'] = platform_id

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)
    platform = platform.first()

    errors = {'text': []}
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


def calendar(request):
    data = get_basic_arguments_for_html_pages(request.user)
    return render(request, 'platforms/calendar.html', data)
