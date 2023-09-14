from django.urls import path
from . import views

urlpatterns = [

    path('purchaseorderinfo/', views.purchaseorderinfo, name='purchaseorderinfo'),
    path('goodsreceiptpoline/', views.goodsreceiptpoline, name='goodsreceiptpoline'),
    
]