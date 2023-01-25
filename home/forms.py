from django import forms
from django.forms.widgets import ClearableFileInput


class Image_form(forms.Form):
    image = forms.ImageField(required=True)


class Contact_form(forms.Form):
    class meta:
        fields = '__all__'

    name = forms.CharField(
        max_length=120, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
