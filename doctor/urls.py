from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.doctor_appointments_list, name='view_appointments'),
    path('appointment/<int:appointment_id>/update/', views.update_appointment, name='update_appointment'),
]
