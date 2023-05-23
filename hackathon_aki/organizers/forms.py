from django import forms
from django.contrib.auth.models import User
from .models import Organizer
from utils import validate_length, validate_charset


class UserOrganizerRegistrationForm(forms.ModelForm):
    length_validation_fields = ['email', 'password', 'first_name', 'last_name']
    charset_validation_fields = ['password', 'first_name', 'last_name']

    repeat_password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': '123456',
    }))

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': '123456',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иван',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванов',
            }),
        }

    def validate(self, error_log):
        is_valid = self.is_valid()
        if not is_valid:
            error_log['email'].append('Некорректный адрес электронной почты.')

        is_valid = validate_length(self.length_validation_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid


class ProfileOrganizerRegistrationForm(forms.ModelForm):
    length_validation_fields = ['middle_name', 'phone_number', 'position', 'juridical_name', 'inn']
    charset_validation_fields = ['middle_name', 'phone_number', 'position', 'juridical_name', 'inn']

    class Meta:
        model = Organizer
        fields = ['middle_name', 'phone_number', 'position', 'juridical_name', 'inn']

        widgets = {
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванович',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (917) 123-45-67',
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Директор',
            }),
            'juridical_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ООО "Яндекс"',
            }),
            'inn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123412341234',
            }),
        }

    def validate(self, error_log):
        is_valid = validate_length(self.length_validation_fields, self.data, error_log)
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid
