# billing/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:appointment_id>/', views.add_or_edit_bill, name='add_bill'),
]
