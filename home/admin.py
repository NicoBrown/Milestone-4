from .models import Profile
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

# Register your models here.

# ...
admin.site.register(Profile)
