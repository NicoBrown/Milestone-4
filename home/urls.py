from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('user_home', views.user_home, name='user_home'),
    path('update_following', views.update_following, name='update_following'),
    path('user_search', views.user_search, name='user_search'),
    path("profile/<int:pk>", views.profile, name="profile"),
    path('onboard_user', views.onboard_user, name='onboard_user'),
    path('contact_form', views.contact_form, name='contact_form'),
]
