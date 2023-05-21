from .models import Client
from django import forms


class ClientRegistrationForm(forms.ModelForm):
    repeat_password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Повторите пароль',
    }))


    class Meta:
        model = Client
        fields = ['e_mail', 'password', 'name', 'surname', 'middle_name', 'phone_number']

        widgets = {
            'e_mail': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Пароль',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия',
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона',
            }),
        }
