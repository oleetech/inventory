from django.db import models
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_svg(value):
    """
    Custom validator to check if the uploaded file is an SVG image.
    """
    if value:
        if not value.name.endswith('.svg'):
            raise ValidationError(
                _('File is not an SVG image.'),
            )

# Create your models here.
class Header(models.Model):
    title = models.CharField(max_length=100,default='',blank=True)    
    logo = models.ImageField(upload_to='website')
    def __str__(self):
        return f" {self.title}"
class Navigation(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)       
    
class IntroSection(models.Model):
    intro_text = HTMLField()
    background_image = models.ImageField(upload_to='website',blank=True, null=True)
    
class AboutUs(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    text = HTMLField()
    image = models.ImageField(upload_to='website',blank=True, null=True,validators=[validate_svg])        