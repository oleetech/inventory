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
    created_date = models.DateTimeField(auto_now_add=True)
    SalesOrder = models.PositiveIntegerField(unique=False)
    CustomerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    Address = models.CharField(max_length=250,blank=True)
    Created = models.DateTimeField(default=timezone.now)
    DocNo = models.PositiveIntegerField(unique=True,default=1)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    TotalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)

    class Meta:

        verbose_name = 'Delivery'
        verbose_name_plural = 'Delivery'

    def __str__(self):
        return f"Delivery for SalesOrderNo {self.DocNo}"


class DeliveryItem(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)   
    Delivery = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    ItemName = models.ForeignKey(Item, on_delete=models.CASCADE,  default=None)
    Quantity = models.PositiveIntegerField(default=0)
    Price = models.DecimalField(max_digits=10, decimal_places=4)
    PriceTotal = models.DecimalField(max_digits=10, decimal_places=4)
    def __str__(self):
        return f"{self.Delivery}" 