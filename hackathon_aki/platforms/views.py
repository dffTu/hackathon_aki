from django.shortcuts import render, redirect
from .models import Platform
from form_utils import get_basic_arguments_for_html_pages


def redirect_to_first_page(request):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


def show_platform_description(request, platform_id):
    data = get_basic_arguments_for_html_pages()
    return render(request, 'platforms/platform_description.html', data)


def show_page(request, page_id):            # Shows catalogue page
    platforms = Platform.objects.all()

    data = get_basic_arguments_for_html_pages()
    data['page_id'] = page_id
    data['platforms'] = platforms

    return render(request, 'platforms/catalogue_page.html', data)
