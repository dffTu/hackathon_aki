from django import forms
from .models import Platform
from utils import validate_length, validate_charset


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class PlatformFileAttachingForm(forms.Form):
    file_field = MultipleFileField(required=False, widget=MultipleFileInput(attrs={
        'class': 'form-control'
    }))


class PlatformCreatingForm(forms.ModelForm):
    length_validation_fields = ['name', 'description']
    charset_validation_fields = ['name', 'description']

    class Meta:
        model = Platform
        fields = ['name', 'description', 'agreement']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
            }),
            'agreement': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def validate(self, error_log):
        is_valid = validate_length(self.length_validation_fields, self.data, error_log)
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid
