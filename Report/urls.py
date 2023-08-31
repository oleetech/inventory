from django.urls import path
from . import views

urlpatterns = [

    
    #Report
    path('receipt_from_production_between_date/', views.receipt_from_production_between_date, name='receipt_from_production_between_date'),

]