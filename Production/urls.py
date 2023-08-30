from django.urls import path
from . import views

urlpatterns = [

    path('ajax/', views.ajax_view, name='ajax_view'),
    path('receiptproduction/', views.ajax_view_receipt, name='receiptproduction'),
]