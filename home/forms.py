from django import forms
from django.forms.widgets import ClearableFileInput


class image_form(forms.Form):
    image = forms.ImageField(required=True)
