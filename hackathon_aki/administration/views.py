from django.shortcuts import redirect
from login_registrate_utils import process_post_forms_requests


@process_post_forms_requests
def redirect_to_first_page(request, data):        # Redirects to first catalogue page
    return redirect('show_page', page_id=1)
