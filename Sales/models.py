from django.db import models
from django.utils import timezone
from BusinessPartners.models import BusinessPartner 
from ItemMasterData.models import Item
# Create your models here.
class SalesOrderInfo(models.Model):
    OrderNumber = models.PositiveIntegerField(default=1, unique=True)
    CustomerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    Address = models.CharField(max_length=50,blank=True)
    Created = models.DateField(default=timezone.now)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)


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