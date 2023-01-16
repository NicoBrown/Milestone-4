from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('expense', views.expense, name='expense'),
    path('<int:expense_id>/', views.expense_detail, name='expense_detail'),
    path('add_expense', views.add_expense, name='add_expense'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('dashboard', views.dashboard, name='dashboard'),
]
