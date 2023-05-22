from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'type': 'email',
        'aria-describedby': 'emailHelp',
        'placeholder': 'name@example.com',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'type': 'password',
        'placeholder': '1234567',
    }))
