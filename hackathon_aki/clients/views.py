import hashlib
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import UserClientRegistrationForm, ProfileClientRegistrationForm
from utils import send_email_for_verify
from form_utils import get_basic_arguments_for_html_pages
from login_registrate_utils import process_post_forms_requests


@process_post_forms_requests
def redirect_to_client_profile(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        return redirect('show_organizer_profile')

    return redirect('show_client_profile')


@process_post_forms_requests
def show_client_profile(request, data):
    if not request.user.is_authenticated:
        return redirect('home')

    if not hasattr(request.user, 'client'):
        return redirect('show_organizer_profile')

    data['email'] = request.user.username

    return render(request, 'clients/profile.html', data)
