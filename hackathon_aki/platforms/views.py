from django.shortcuts import render, redirect
from .models import Platform
from form_utils import get_basic_arguments_for_html_pages


def redirect_to_first_page(request):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


def show_page(request, page_id):            # Shows catalogue page
    platforms = Platform.objects.all()

    data = get_basic_arguments_for_html_pages(request)
    data['page_id'] = page_id
    data['platforms'] = platforms

    return render(request, 'platforms/catalogue_page.html', data)


def show_platform_description(request, platform_id):
    data = get_basic_arguments_for_html_pages(request)
    data['platform_id'] = platform_id

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)

    return render(request, 'platforms/platform_description.html', data)


def leave_comment(request, platform_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'client'):
        return redirect('show_platform_description', platform_id=platform_id)

    data = get_basic_arguments_for_html_pages(request)
    data['platform_id'] = platform_id

    platform = Platform.objects.filter(id=platform_id)
    if not platform.exists():
        return render(request, 'platforms/platform_not_found.html', data)
    platform = platform.first()

    print(platform)

    errors = {'name': [],
              'description': []}

    data = get_basic_arguments_for_html_pages(request)
    data['platform_id'] = platform_id
    return render(request, 'platforms/platform_description.html', data)
