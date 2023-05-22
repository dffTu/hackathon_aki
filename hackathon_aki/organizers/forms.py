from django import forms
from django.contrib.auth.models import User
from .models import Organizer


class UserOrganizerRegistrationForm(forms.ModelForm):
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


class ProfileOrganizerRegistrationForm(forms.ModelForm):
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
