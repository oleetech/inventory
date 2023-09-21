from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_payroll/', views.upload_payroll, name='upload_payroll'),
    path('upload_attendance/', views.upload_attendance, name='upload_attendance'),
    path('upload_overtime_record/', views.upload_overtime_record, name='upload_overtime_record'),
    
    # path('attendance_report/', views.attendance_report, name='attendance_report'),

  


]