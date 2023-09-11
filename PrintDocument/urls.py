from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='print'),
    path('salesOrder', views.salesOrder, name='salesOrder'),
    path('delivery', views.delivery, name='delivery'),
    


]