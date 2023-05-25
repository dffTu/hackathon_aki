from django import forms
from utils import validate_length


class LoginForm(forms.Form):
    required_fields = ['email', 'password']

    email = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'email',
        'placeholder': 'name@example.com',
    }))
    password = forms.CharField(max_length=250, required=False, widget=forms.PasswordInput(attrs={
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
