from django import forms
from utils import validate_length, validate_charset


class PasswordResetForm(forms.Form):
    required_fields = ['password']
    length_validation_fields = ['password']
    charset_validation_fields = ['password']

    password = forms.CharField(max_length=250, required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': '123456',
    }))
    repeat_password = forms.CharField(max_length=250, required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': '123456',
    }))

    def validate(self, error_log):
        is_valid = self.is_valid()
        if not is_valid:
            error_log['incorrect_form'] = True

        is_valid = validate_length(self.length_validation_fields, self.required_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid


class LoginForm(forms.Form):
    required_fields = ['email', 'password']

    email = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'email',
        'placeholder': 'name@example.com',
    }))
    password = forms.CharField(max_length=250, required=False, widget=forms.PasswordInput(attrs={
        'id': 'login_form_password',
        'class': 'form-control',
        'type': 'password',
        'placeholder': '123456',
    }))

    def validate(self, error_log):
        is_valid = self.is_valid()
        if not is_valid:
            error_log['incorrect_form'] = True

        is_valid = validate_length([], self.required_fields, self.data, error_log) and is_valid
        return is_valid
