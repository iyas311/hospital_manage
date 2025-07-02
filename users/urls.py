from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doctor-profile/<int:user_id>/', views.edit_doctor_profile, name='edit_doctor_profile'),
    path('patient-profile/<int:user_id>/', views.edit_patient_profile, name='edit_patient_profile'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
]
