from django.urls import path
from . import views

urlpatterns = [
    path('appointment/book/', views.book_appointment, name='book_appointment'),
    path('medical-history/', views.medical_history, name='medical_history'),
    path('billing/', views.billing, name='billing'),
     path('billing/pay/<int:bill_id>/', views.pay_bill, name='pay_bill'),
]
