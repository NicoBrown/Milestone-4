from django import forms
from django.forms.widgets import ClearableFileInput
from django.core.validators import FileExtensionValidator


class Image_form(forms.Form):
    image = forms.ImageField(required=True, validators=[FileExtensionValidator(
        ['gif', 'tif', 'jpg', 'jpeg', 'png', 'bmp', 'webp'])])


class Contact_form(forms.Form):
    class meta:
        fields = '__all__'

    name = forms.CharField(
        max_length=120, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
