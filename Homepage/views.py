from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Header, Navigation, IntroSection, AboutUs

def home(request):
    # Retrieve objects from your models
    header = Header.objects.first()
    navigation = Navigation.objects.all()
    intro_section = IntroSection.objects.first()
    about_us = AboutUs.objects.first()
    
    # Create a context dictionary with the data
    context = {
        'header': header,
        'navigation': navigation,
        'intro_section': intro_section,
        'about_us': about_us,
    }        
    return render(request, 'home.html',context)