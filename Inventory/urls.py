"""
URL configuration for Inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Import your views

from django.views.generic import TemplateView
class HomeView(TemplateView):
    template_name = 'home.html'  
admin.site.site_header = "OleeTech"
admin.site.site_title = "OleeTech Industry Automation System"
admin.site.index_title = ""
urlpatterns = [
    path('', HomeView.as_view(), name='home'),    
    path('admin/', admin.site.urls),
    path('select2/', include('django_select2.urls', namespace='django_select2')),
    path('production/',include('Production.urls')),   
    path('sales/',include('Sales.urls')),    
    path('itemMasterData/',include('ItemMasterData.urls')),     
 
    path('report/',include('Report.urls')),  
    path('send_data/', views.send_data, name='send_data'),
      
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)