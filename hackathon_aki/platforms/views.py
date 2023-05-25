from django.shortcuts import render, redirect
from .models import Platform, Comment
from main.models import CommentAttachment
from .forms import CommentFileAttachingForm, CommentLeavingForm
from login_registrate_utils import process_post_forms_requests
from .search_utils import search_platforms
from calendar_utils import Month, build_calendar



@process_post_forms_requests
def redirect_to_first_page(request, data):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


@process_post_forms_requests
def show_page(request, data, page_id):            # Shows catalogue page
    relevant_platforms_list = Platform.objects.all()
    data['search'] = ''
    if 'search' in request.GET and request.GET['search'] != '':
        relevant_platforms_list = []
        platform_names = [platform.name for platform in Platform.objects.all()]
        result_platforms = search_platforms(request.GET['search'], platform_names)
        for platform_name in result_platforms:
            for platform in Platform.objects.filter(name=platform_name):
                if platform in relevant_platforms_list:
                    continue
                relevant_platforms_list.append(platform)
        data['search'] = request.GET['search']

    number_of_platforms = 0
    if 'platform_categories' not in request.GET or not request.GET['platform_categories']:
        data['page_id'] = page_id
        data['platforms'] = [[]]
        number_of_platforms = len(relevant_platforms_list)
        for platform in relevant_platforms_list:
            if len(data['platforms'][-1]) == 3:
                data['platforms'].append([])
            data['platforms'][-1].append(platform)
        data['filter_request'] = ''
    else:
        categories = request.GET['platform_categories'].split(';')
        data['platforms'] = [[]]
        for platform in relevant_platforms_list:
            current_platform_categories = platform.categories.split(';')
            should_add = False
            for current_platform_category in current_platform_categories:
                if current_platform_category in categories:
                    should_add = True
                    break
            if should_add:
                if len(data['platforms'][-1]) == 3:
                    data['platforms'].append([])
                data['platforms'][-1].append(platform)
                number_of_platforms += 1

        data['page_id'] = page_id
        data['filter_request'] = request.GET['platform_categories']

    data['all_pages'] = list(range(1, (number_of_platforms + 14) // 15 + 1))

    return render(request, 'platforms/catalogue_page.html', data)


@process_post_forms_requests
def show_platform_description(request, data, platform_id):
    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
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
