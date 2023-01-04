from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('user_home', views.user_home, name='user_home'),
    path('user_search', views.user_search, name='user_search'),
    path('user_following/<int:pk>',
         views.update_following, name='update_following'),
    path("profile/<int:pk>", views.profile, name="profile"),
]
