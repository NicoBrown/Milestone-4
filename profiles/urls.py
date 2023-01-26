from profiles import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("edit_profile",
         views.edit_profile, name="edit_profile"),
    path("delete_profile/<int:profile_id>",
         views.delete_profile, name="delete_profile"),
    path('update_following', views.update_following, name='update_following'),
    path('user_search', views.user_search, name='user_search'),
]
