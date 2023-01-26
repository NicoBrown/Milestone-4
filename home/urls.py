from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('user_home', views.user_home, name='user_home'),
    path('onboard_user', views.onboard_user, name='onboard_user'),
    path('contact_form', views.contact_form, name='contact_form'),
]
