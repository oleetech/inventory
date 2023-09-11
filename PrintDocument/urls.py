from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('salesOrder', views.salesOrder, name='salesOrder'),
    


]