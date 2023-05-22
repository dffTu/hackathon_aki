from django.shortcuts import render, redirect
from .models import Platform


def redirect_to_first_page(request):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


def show_page(request, page_id):            # Shows catalogue page
    platforms = Platform.objects.all()
    return render(request, 'platforms/catalogue_page.html', {'page_id': page_id, 'platforms': platforms})
