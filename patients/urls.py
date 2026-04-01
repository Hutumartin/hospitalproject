from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('add/', views.patient_add, name='patient_add'),
    path('edit/<int:pk>/', views.patient_edit, name='patient_edit'),
    path('delete/<int:pk>/', views.patient_delete, name='patient_delete'),
    path('records/<int:pk>/', views.patient_records, name='patient_records'),
    path('records/<int:pk>/upload/', views.record_upload, name='record_upload'),
    path('records/delete/<int:pk>/', views.record_delete, name='record_delete'),
]