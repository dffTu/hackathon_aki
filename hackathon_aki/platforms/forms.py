from django import forms
from .models import Platform
from utils import validate_length, validate_charset


class PlatformCreatingForm(forms.ModelForm):
    length_validation_fields = ['name', 'description']
    charset_validation_fields = ['name', 'description']

    class Meta:
        model = Platform
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
            }),
        }

    def validate(self, error_log):
        is_valid = validate_length(self.length_validation_fields, self.data, error_log)
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid
