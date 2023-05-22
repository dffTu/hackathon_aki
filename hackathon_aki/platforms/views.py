from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PlatformCreatingForm


def redirect_to_first_page(request):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)


def create_platform(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'organizer'):
        return redirect('home')

    if request.method == 'POST':
        form = PlatformCreatingForm(request.POST)
        print(form.is_valid(), form.errors)
        if form.is_valid():
            platform = form.save(commit=False)
            platform.organizer = request.user.organizer
            platform.save()

            return HttpResponse('congrats')
        else:
            return HttpResponse('!#@$#@#')

    return render(request, 'platforms/create_platform.html', {'form': PlatformCreatingForm()})


def show_page(request, page_id):            # Shows catalogue page
    data = {'page_id': page_id}
    return render(request, 'platforms/catalogue_page.html', data)
