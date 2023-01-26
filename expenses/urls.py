from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add_image', views.add_image, name='add_image'),
    path('add_expense', views.add_expense, name='add_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]
