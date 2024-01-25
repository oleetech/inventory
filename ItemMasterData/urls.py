from django.urls import path,include
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'',views.ItemViewSet)
urlpatterns = [

    path('item/', views.item, name='item'),
    path('item_name/', views.item_name, name='item_name'),
    path('items/', include(router.urls)),  
    path('autocomplete/', views.AutocompleteView.as_view(), name='autocomplete'),
  
]