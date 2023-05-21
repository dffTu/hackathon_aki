from django import forms
from django.contrib.auth.models import User
from .models import Client


class UserClientRegistrationForm(forms.ModelForm):
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


class ProfileClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['middle_name', 'phone_number']

        widgets = {
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона',
            }),
        }
