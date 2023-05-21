from django.shortcuts import render, redirect


def redirect_to_first_page(request):        # Redirects to first catalogue page
    return redirect('/catalogue/page/1')


def show_page(request, page_id):            # Shows catalogue page
    data = {'page_id': page_id}
    return render(request, 'platforms/catalogue_page.html', data)
