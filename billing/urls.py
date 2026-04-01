from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing_list, name='billing_list'),
    path('add/', views.billing_add, name='billing_add'),
    path('edit/<int:pk>/', views.billing_edit, name='billing_edit'),
    path('delete/<int:pk>/', views.billing_delete, name='billing_delete'),
    path('invoice/<int:pk>/', views.billing_invoice, name='billing_invoice'),
]