from django.db import models
from ItemMasterData.models import Item
from GeneralSettings.models import Unit
# Create your models here.
class BillOfMaterials(models.Model):
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)


class ChildComponent(models.Model):
    bill_of_materials = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name='child_components')
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    
'''
  ____                       _                  _     _                      ___               _               
 |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __      / _ \   _ __    __| |   ___   _ __ 
 | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \    | | | | | '__|  / _` |  / _ \ | '__|
 |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |   | |_| | | |    | (_| | |  __/ | |   
 |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|    \___/  |_|     \__,_|  \___| |_|   
                                                                                                               
'''
from datetime import date


from Sales.models import SalesOrderInfo,SalesOrderItem
class Production(models.Model):
    Status_CHOICES = [
        ('P', 'Planned'),
        ('R', 'Released'),
        ('C', 'Close'),
        ('F', 'Canceled')
        
    ]
    status = models.CharField(max_length=1, choices=Status_CHOICES,default='P')
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    sales_order_no = models.PositiveIntegerField(default=1)
    created_date = models.DateField(default=date.today)
    order_date = models.DateField(default=date.today)
    start_date = models.DateField(default=date.today)
    due_date = models.DateField(default=date.today)
    docno = models.PositiveIntegerField(unique=True,default=1)
    

        
    def __str__(self):
        return f"{self.docno}"

class ProductionComponent(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='production_components')
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    uom =  models.CharField(max_length=100,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name   
    
    
    
'''
  ____                         _           _       _____                                ____                       _                  _     _                 
 |  _ \    ___    ___    ___  (_)  _ __   | |_    |  ___|  _ __    ___    _ __ ___     |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __  
 | |_) |  / _ \  / __|  / _ \ | | | '_ \  | __|   | |_    | '__|  / _ \  | '_ ` _ \    | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \ 
 |  _ <  |  __/ | (__  |  __/ | | | |_) | | |_    |  _|   | |    | (_) | | | | | | |   |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |
 |_| \_\  \___|  \___|  \___| |_| | .__/   \__|   |_|     |_|     \___/  |_| |_| |_|   |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|
                                  |_|                                                                                                                         
'''

class ProductionReceipt(models.Model):
    receiptNumber = models.PositiveIntegerField(default=1, unique=True)
    created = models.DateField(default=date.today)
    def __str__(self):
        return f"ReceiptNo{self.ReceiptNumber}"


            
            
class ProductionReceiptItem(models.Model):
    receiptNumber = models.ForeignKey(ProductionReceipt, on_delete=models.CASCADE, null=True, default=None)
    salesOrderItem = models.PositiveIntegerField(default=1)
    productionNo =  models.PositiveIntegerField(default=1)
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4)
    size = models.CharField(max_length=50,default='')
    color = models.CharField(max_length=50,default='')
    def __str__(self):
        return f": {self.ReceiptNumber}"    