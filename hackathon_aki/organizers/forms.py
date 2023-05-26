from django import forms
from django.contrib.auth.models import User
from .models import Organizer
from platforms.models import FreeSlot
from main.models import EmailVerification
from utils import validate_length, validate_charset


class UserOrganizerRegistrationForm(forms.ModelForm):
    required_fields = ['email', 'password', 'first_name', 'last_name']
    length_validation_fields = ['email', 'password', 'first_name', 'last_name']
    charset_validation_fields = ['password', 'first_name', 'last_name']

    repeat_password = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': '123456',
    }))

    class Meta:
        model = EmailVerification
        fields = ['email', 'password', 'first_name', 'last_name']

        widgets = {
            'email': forms.TextInput(attrs={
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
            error_log['incorrect_form'] = True

        is_valid = validate_length(self.length_validation_fields, self.required_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid


class ProfileOrganizerRegistrationForm(forms.ModelForm):
    required_fields = ['phone_number']
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
        is_valid = self.is_valid()
        if not is_valid:
            error_log['incorrect_form'] = True

        is_valid = validate_length(self.length_validation_fields, self.required_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid


class UserOrganizerChangingForm(forms.ModelForm):
    required_fields = ['first_name', 'last_name']
    length_validation_fields = ['first_name', 'last_name']
    charset_validation_fields = ['first_name', 'last_name']

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

        widgets = {
            'email': forms.TextInput(attrs={
                'immutable': True,
                'class': 'form-control',
                'placeholder': 'name@example.com',
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
            error_log['incorrect_form'] = True

        is_valid = validate_length(self.length_validation_fields, self.required_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid


class FreeSlotAddingForm(forms.ModelForm):
    required_fields = ['date', 'price']

    class Meta:
        model = FreeSlot
        fields = ['date', 'price']

        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена',
            }),
        }

    def validate(self, error_log):
        is_valid = self.is_valid()
        if not is_valid:
            error_log['incorrect_form'] = True

        is_valid = validate_length([], self.required_fields, self.data, error_log) and is_valid
        return is_valid
