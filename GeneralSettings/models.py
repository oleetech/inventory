from django.db import models

# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=100,unique=True)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
    
class CompanyInfoManager(models.Manager):
    def get_or_create_single(self, defaults=None, **kwargs):
        instance, created = self.get_or_create(**kwargs, defaults=defaults)
        return instance

class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20,default=0)
    email = models.EmailField(default='')
    website = models.URLField(default='')
    established_year = models.PositiveIntegerField(default=1)


    objects = CompanyInfoManager()

    def save(self, *args, **kwargs):
        # Ensure that only one instance exists
        if Company.objects.exists() and not self.pk:
            raise ValueError("Only one CompanyInfo instance can be created.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the instance
        pass

    class Meta:
        verbose_name_plural = "Company Information"    
        
    def __str__(self):
        return self.name        
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="The name of the department")
    description = models.TextField(blank=True, null=True, help_text="A description of the department")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the department was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the department was last updated")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Departments"        
