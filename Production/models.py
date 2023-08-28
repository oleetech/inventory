from django.db import models
from ItemMasterData.models import Item
from GeneralSettings.models import Unit
# Create your models here.
class BillOfMaterials(models.Model):

    name = models.ForeignKey(Item, on_delete=models.CASCADE,  default=None)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)


class ChildComponent(models.Model):
    bill_of_materials = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name='child_components')

    name = models.ForeignKey(Item, on_delete=models.CASCADE,  default=None)
    uom = models.ForeignKey(Unit, on_delete=models.CASCADE,  default=None)
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

    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    sales_order_no = models.ForeignKey(SalesOrderInfo,on_delete=models.CASCADE,related_name='sales_production_order',default=1)
    created_date = models.DateField(default=date.today)
    order_date = models.DateField(default=date.today)
    start_date = models.DateField(default=date.today)
    due_date = models.DateField(default=date.today)
    docno = models.PositiveIntegerField(unique=True,default=1)
    

        
    def __str__(self):
        return f"{self.docno}"

class ProductionComponent(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='production_components')
    name = models.CharField(max_length=100)
    uom = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return self.name   
    