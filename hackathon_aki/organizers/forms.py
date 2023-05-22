from django import forms
from django.contrib.auth.models import User
from .models import Organizer
from utils import validate_unique, validate_length, validate_charset


class UserOrganizerRegistrationForm(forms.ModelForm):
    unique_fields = {'username': 'email'}
    length_validation_fields = ['email', 'password', 'first_name', 'last_name']
    charset_validation_fields = ['password', 'first_name', 'last_name']

    repeat_password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': 'Повторите пароль',
    }))

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Пароль',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия',
            }),
        }

    def validate(self, form_data, error_log):
        is_valid = validate_unique(self.unique_fields, form_data, User, error_log)
        is_valid = validate_length(self.length_validation_fields, form_data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, form_data, error_log) and is_valid
        return is_valid


class ProfileOrganizerRegistrationForm(forms.ModelForm):
    unique_fields = {'phone_number': 'phone_number'}
    length_validation_fields = ['middle_name', 'phone_number', 'position', 'juridical_name', 'inn']
    charset_validation_fields = ['middle_name', 'phone_number', 'position', 'juridical_name', 'inn']

    class Meta:
        model = Organizer
        fields = ['middle_name', 'phone_number', 'position', 'juridical_name', 'inn']

        widgets = {
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона',
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Должность',
            }),
            'juridical_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название юридичиского лица',
            }),
            'inn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ИНН',
            }),
        }

    def validate(self, form_data, error_log):
        is_valid = validate_unique(self.unique_fields, form_data, User, error_log)
        is_valid = validate_length(self.length_validation_fields, form_data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, form_data, error_log) and is_valid
        return is_valid
