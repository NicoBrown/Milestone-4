from django import forms
from .models import User, UserProfile


class User_edit_form(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name']


class Profile_edit_form(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['default_phone_number', 'default_postcode']
