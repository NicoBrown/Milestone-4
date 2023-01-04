from django.contrib import admin
from profiles.models import UserProfile
from django.contrib.auth.models import User, Group

# Register your models here.


class ProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name"]
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
