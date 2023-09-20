from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('policestation/', views.policestation, name='policestation'),
    path('upload_payroll/', views.upload_payroll, name='upload_payroll'),

  


]