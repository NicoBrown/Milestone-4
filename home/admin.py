from .models import profiles
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


# Register your models here.

# ...
admin.site.register(profiles)


class ProfileInline(admin.StackedInline):
    model = profiles


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
