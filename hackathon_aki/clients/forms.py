from .models import Client
from django.forms import ModelForm, TextInput, EmailInput


class ClientRegistrationForm(ModelForm):
    class Meta:
        model = Client
        fields = ['e_mail', 'password', 'name', 'surname', 'middle_name', 'phone_number']

        widgets = {
            'e_mail': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Пароль',
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
            }),
            'surname': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия',
            }),
            'middle_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество',
            }),
            'phone_number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона',
            }),
        }
