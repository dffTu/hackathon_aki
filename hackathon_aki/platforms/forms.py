from django import forms
from .models import Platform, Comment
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


class CalendarImportingForm(forms.Form):
    file_field = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'id': 'calendar_importing_file_field',
        'class': 'form-control calendar-importing-file-field',
        'accept': '.xlsx'
    }))


class PlatformFileAttachingForm(forms.Form):
    file_field = MultipleFileField(required=False, widget=MultipleFileInput(attrs={
        'class': 'form-control',
        'accept': 'image/*'
    }))


class PlatformCreatingForm(forms.ModelForm):
    required_fields = ['name', 'short_description']
    length_validation_fields = ['name', 'short_description', 'description']
    charset_validation_fields = ['name', 'short_description', 'description']

    address = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите адрес',
        'id': "address_suggest_form",
    }))

    class Meta:
        model = Platform
        fields = ['name', 'short_description', 'description', 'agreement']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Краткое описание',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
            }),
            'agreement': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*, .pdf'
            }),
        }

    def validate(self, error_log):
        is_valid = self.is_valid()
        if not is_valid:
            error_log['incorrect_form'] = True

        is_valid = validate_length(self.length_validation_fields, self.required_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid


class CommentFileAttachingForm(forms.Form):
    file_field = MultipleFileField(required=False, widget=MultipleFileInput(attrs={
        'class': 'form-control',
        'accept': 'image/*'
    }))


class CommentLeavingForm(forms.ModelForm):
    required_fields = ['text']
    length_validation_fields = ['text']
    charset_validation_fields = ['text']

    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст отзыва',
            })
        }

    def validate(self, error_log):
        is_valid = self.is_valid()
        if not is_valid:
            error_log['incorrect_form'] = True

        is_valid = validate_length(self.length_validation_fields, self.required_fields, self.data, error_log) and is_valid
        is_valid = validate_charset(self.charset_validation_fields, self.data, error_log) and is_valid
        return is_valid
