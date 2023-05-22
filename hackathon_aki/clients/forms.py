from django import forms
from django.contrib.auth.models import User
from .models import Client
from utils import validate_unique, validate_length, validate_charset


class UserClientRegistrationForm(forms.ModelForm):
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
        is_valid = validate_unique(self.unique_fields, self.data, self._meta.model, error_log)
        is_valid = validate_length(self.length_validation_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid


class ProfileClientRegistrationForm(forms.ModelForm):
    unique_fields = {'phone_number': 'phone_number'}
    length_validation_fields = ['middle_name', 'phone_number']
    charset_validation_fields = ['middle_name', 'phone_number']

    class Meta:
        model = Client
        fields = ['middle_name', 'phone_number']

        widgets = {
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванович',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (917) 123-45-67',
            }),
        }

    def validate(self, error_log):
        is_valid = validate_unique(self.unique_fields, self.data, self._meta.model, error_log)
        is_valid = validate_length(self.length_validation_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid
