from main.forms import LoginForm
from clients.forms import UserClientRegistrationForm, ProfileClientRegistrationForm
from organizers.forms import UserOrganizerRegistrationForm, ProfileOrganizerRegistrationForm
from utils import platform_categories


def get_basic_arguments_for_html_pages(request):
    data = {
        'login_form': LoginForm(),
        'user_client_registration_form': UserClientRegistrationForm(),
        'profile_client_registration_form': ProfileClientRegistrationForm(),
        'user_organizer_registration_form': UserOrganizerRegistrationForm(),
        'profile_organizer_registration_form': ProfileOrganizerRegistrationForm(),
        'error_message': '',
        'filters': {},
        'platform_categories': platform_categories,
        'url_path': request.path,
        'drop_localstorage': True,
    }
    if request.user.is_authenticated:
        data['user_fields'] = request.user
    return data
