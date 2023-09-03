from os import name
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from GeneralSettings.models import Unit
from datetime import date

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    # Add any other fields for the Warehouse model

    def __str__(self):
        return self.name


class Item(models.Model):
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    description = models.TextField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, default=1)
    unit = models.ForeignKey(Unit, on_delete=models.SET_DEFAULT, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
    # Add any other fields you need
        verbose_name = 'Item Master Data'
        verbose_name_plural = 'Item Master Data'    
    def __str__(self):
        return self.name


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class ItemReceiptinfo(models.Model):

    docno = models.PositiveIntegerField(default=1, unique=True)
    created = models.DateTimeField(default=timezone.now)
    
    class Meta:
    
        verbose_name = 'Goods Receipt'
        verbose_name_plural = 'Goods Receipt'
    def __str__(self):
        return " {}".format(self.docno)


class ItemReceipt(models.Model):
    item_info = models.ForeignKey(ItemReceiptinfo, on_delete=models.CASCADE, null=True, default=None)
    created = models.DateField(default=date.today, editable=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.created:            
            self.created = self.item_info.created
                   
        super().save(*args, **kwargs)   
        
    def __str__(self):
        return " {}".format(self.item_info.docno)

    def clean(self):
        if self.quantity == 0:
            raise ValidationError("Quantity cannot be 0.")


class ItemDeliveryinfo(models.Model):
    
    docno = models.PositiveIntegerField(default=1, unique=True)
    created = models.DateTimeField(default=timezone.now)
    
    class Meta:
        
        verbose_name = 'Goods Delivery'
        verbose_name_plural = 'Goods Delivery'
    def __str__(self):
        return " {}".format(self.docno)


class ItemDelivery(models.Model):
    created = models.DateField(default=date.today, editable=True)
    
    item_info = models.ForeignKey(ItemDeliveryinfo, on_delete=models.CASCADE, null=True, default=None)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.created:         
            self.created = self.item_info.created
                   
        super().save(*args, **kwargs)   
    def __str__(self):
        return "ItemDelivery: {} - {}".format(self.item.name, self.quantity)