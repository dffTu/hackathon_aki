from django.shortcuts import render, redirect
from .forms import PlatformCreatingForm


def redirect_to_first_page(request):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


def create_platform(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    errors = {'name': [],
              'description': []}

    if request.method == 'POST':
        form = PlatformCreatingForm(request.POST)
        if form.validate(errors):
            platform = form.save(commit=False)
            platform.organizer = request.user.organizer
            platform.rating = 5
            platform.save()

            return redirect('show_organizer_platforms')

    return render(request, 'platforms/create_platform.html', {'form': PlatformCreatingForm(),
                                                              'errors': errors})


def show_page(request, page_id):            # Shows catalogue page
    return render(request, 'platforms/catalogue_page.html', {'page_id': page_id})
