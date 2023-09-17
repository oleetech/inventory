from django.db import models
from django.utils import timezone
from BusinessPartners.models import BusinessPartner 
from ItemMasterData.models import Item
from Sales.models import SalesEmployee
from datetime import date
from django.contrib.auth.models import User
class IncomingPaymentInfo(models.Model):
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.CASCADE, default=0,null=True, blank=True,)  # Set the default to an existing SalesEmployee or a specific ID
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    remarks = models.CharField(max_length=250,default='',blank=True)
    
    class Meta:

        verbose_name = 'Incoming Payment'
        verbose_name_plural = 'Incoming Payment'
        
    def __str__(self):
        return f"{self.docNo}"    
    
    
    
    
    
class OutgoingPaymentInfo(models.Model):
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.CASCADE, default=0,null=True, blank=True,)  # Set the default to an existing SalesEmployee or a specific ID
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    remarks = models.CharField(max_length=250,default='',blank=True)
    
    class Meta:

        verbose_name = 'Outgoing Payment'
        verbose_name_plural = 'Outgoing Payment'
        
    def __str__(self):
        return f"{self.docNo}"        