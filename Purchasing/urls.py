from django.urls import path
from . import views

urlpatterns = [

    path('purchaseorderinfo/', views.purchaseorderinfo, name='purchaseorderinfo'),
    path('goodsreceiptpoline/', views.goodsreceiptpoline, name='goodsreceiptpoline'),
    path('goodsreReiptPoinfo/', views.goodsreReiptPoinfo, name='goodsreReiptPoinfo'),   
    path('goodsreceiptpoline/', views.goodsreceiptpoline, name='goodsreceiptpoline'),  
    
]