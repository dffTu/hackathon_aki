from django import forms
from .models import Client
from main.models import EmailVerification
from utils import validate_length, validate_charset


class UserClientRegistrationForm(forms.ModelForm):
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


class ProfileClientRegistrationForm(forms.ModelForm):
    required_fields = ['phone_number']
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
        is_valid = self.is_valid()
        if not is_valid:
            error_log['incorrect_form'] = True

        is_valid = validate_length(self.length_validation_fields, self.required_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid


class UserClientChangingForm(forms.ModelForm):
    required_fields = ['first_name', 'last_name']
    length_validation_fields = ['first_name', 'last_name']
    charset_validation_fields = ['first_name', 'last_name']

    class Meta:
        model = EmailVerification
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
