from django.urls import path
from . import views

urlpatterns = [

    path('delivery/', views.ajax_view, name='delivery'),

]