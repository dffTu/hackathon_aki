from django.shortcuts import redirect
from platforms.models import Platform
from login_registrate_utils import process_post_forms_requests, show_catalogue_page


@process_post_forms_requests
def redirect_to_first_page(request, data):        # Redirects to first catalogue page
    return redirect('show_unverified_page', page_id=1)


@process_post_forms_requests
def show_unverified_page(request, data, page_id):            # Shows catalogue page
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('show_page', page_id=page_id)

    data['catalogue_type'] = 'show_unverified_page'
    relevant_platforms_list = Platform.objects.filter(verified=False)
    return show_catalogue_page(request, data, page_id, relevant_platforms_list)
