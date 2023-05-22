from django import forms
from .models import Platform


class PlatformCreatingForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ['name', 'description', 'rating']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }
