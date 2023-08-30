from django.db import models
from django.utils import timezone
from BusinessPartners.models import BusinessPartner 
from ItemMasterData.models import Item


# Create your models here.
class SalesOrderInfo(models.Model):
    OrderNumber = models.PositiveIntegerField(default=1, unique=True)
    CustomerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    Address = models.CharField(max_length=250,blank=True)
    Created = models.DateField(default=timezone.now)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)

    class Meta:

        verbose_name = 'Order'
        verbose_name_plural = 'Order'
        
    def __str__(self):
        return f"{self.OrderNumber}"

class SalesOrderItem(models.Model):
    OrderNumber = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE, null=True, default=None)
    
    ItemName = models.ForeignKey(Item, on_delete=models.CASCADE,  default=None)
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=4)
    PriceTotal = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f": {self.OrderNumber}"
    
    
'''
  ____           _   _                               
 |  _ \    ___  | | (_) __   __   ___   _ __   _   _ 
 | | | |  / _ \ | | | | \ \ / /  / _ \ | '__| | | | |
 | |_| | |  __/ | | | |  \ V /  |  __/ | |    | |_| |
 |____/   \___| |_| |_|   \_/    \___| |_|     \__, |
                                               |___/ 
'''

class DeliveryInfo(models.Model):
    salesOrder = models.PositiveIntegerField(unique=False)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateTimeField(default=timezone.now)
    docNo = models.PositiveIntegerField(unique=True,default=1)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)

    class Meta:

        verbose_name = 'Delivery'
        verbose_name_plural = 'Delivery'

    def __str__(self):
        return f"Delivery for SalesOrderNo {self.docNo}"


class DeliveryItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)   
    delivery = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4)
    def __str__(self):
        return f"{self.Delivery}" 
    
    
class SalesQuotetionInfo(models.Model):
    docNumber = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)

    class Meta:

        verbose_name = 'Sales Quotetion'
        verbose_name_plural = 'Sales Quotetion'
        
    def __str__(self):
        return f"{self.docNumber}"   
    

class SalesQuotetionItem(models.Model):
    docNumber = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE, null=True, default=None)
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f": {self.docNumber}"    