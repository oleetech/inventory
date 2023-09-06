

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
    
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = HTMLField() # Change This Line
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    logo = models.ImageField(upload_to='reportlogo/', null=True, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title  
    
    def save(self, *args, **kwargs):
        # If the author is not set, set it to the current user
        if not self.author_id:
            self.author = User.objects.get(username='current_user_username')
        super().save(*args, **kwargs)
        
        
        verbose_name = ''
        verbose_name_plural = ''           
        


