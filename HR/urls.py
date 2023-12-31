from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homehr'),
    path('upload_payroll/', views.upload_payroll, name='upload_payroll'),
    path('upload_attendance/', views.upload_attendance, name='upload_attendance'),
    path('upload_overtime_record/', views.upload_overtime_record, name='upload_overtime_record'),
    path('leave_balance_report/', views.leave_balance_report, name='leave_balance_report'),
    path('overtime_summary_report/', views.overtime_summary_report, name='overtime_summary_report'),
    path('overtime_summary_report_machine/', views.overtime_summary_report_machine, name='overtime_summary_report_machine'),
    
    path('employee_leave_records_report/', views.employee_leave_records_report, name='employee_leave_records_report'),
    path('employee_ot_hour_records_report/', views.employee_ot_hour_records_report, name='employee_ot_hour_records_report'),
    path('update_holidays_status_view/', views.update_holidays_status_view, name='update_holidays_status_view'),
    
    path('attendance_report/', views.attendance_report, name='attendance_report'),
    path('present_records_between_date/', views.present_records_between_date, name='present_records_between_date'),
    path('employees_without_present_records/', views.employees_without_present_records, name='employees_without_present_records'),
    path('resignation_records_between_dates/', views.resignation_records_between_dates, name='resignation_records_between_dates'),
    path('lefty_records_between_dates/', views.lefty_records_between_dates, name='lefty_records_between_dates'),
    path('leave_request_records_between_dates/', views.leave_request_records_between_dates, name='leave_request_records_between_dates'),

    path('job_card/', views.job_card, name='job_card'),
    path('job_card_summary/', views.job_card_summary, name='job_card_summary'),
    
    #print id card
    path('select_employees/', views.select_employees, name='select_employees'),
  


]