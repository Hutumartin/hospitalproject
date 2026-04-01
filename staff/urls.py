from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_list, name='staff_list'),
    path('add/', views.staff_add, name='staff_add'),
    path('edit/<int:pk>/', views.staff_edit, name='staff_edit'),
    path('delete/<int:pk>/', views.staff_delete, name='staff_delete'),
]