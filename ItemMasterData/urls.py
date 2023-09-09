from django.urls import path
from . import views

urlpatterns = [

    path('item/', views.item, name='item'),
    path('item_name/', views.item_name, name='item_name'),
    
]