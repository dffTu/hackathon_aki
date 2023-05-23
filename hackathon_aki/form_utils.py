from main.forms import LoginForm
from clients.forms import UserClientRegistrationForm, ProfileClientRegistrationForm
from organizers.forms import UserOrganizerRegistrationForm, ProfileOrganizerRegistrationForm


def get_basic_arguments_for_html_pages(user):
    data = {
        'login_form': LoginForm(),
        'user_client_registration_form': UserClientRegistrationForm(),
        'profile_client_registration_form': ProfileClientRegistrationForm(),
        'user_organizer_registration_form': UserOrganizerRegistrationForm(),
        'profile_organizer_registration_form': ProfileOrganizerRegistrationForm(),
        'error_message': '',
    }
    if user.is_authenticated:
        data['user_fields'] = user
    return data
