from django.db import models
from ItemMasterData.models import Item
from GeneralSettings.models import Unit,Department
from datetime import date
from django.contrib.auth.models import User
from django.db.models import Sum
from Sales.models import SalesOrderItem

# Create your models here.
class BillOfMaterials(models.Model):
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
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
    uom =  models.CharField(max_length=100,default='',null=True)    
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    salesOrder = models.PositiveIntegerField(default=1)
    created = models.DateField(default=date.today, editable=True)
    order_date = models.DateField(default=date.today)
    start_date = models.DateField(default=date.today)
    due_date = models.DateField(default=date.today)
    docno = models.PositiveIntegerField(unique=True,default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    remarks = models.CharField(max_length=250,default='',blank=True)
  
    class Meta:

        verbose_name = ' Production Order'
        verbose_name_plural = 'Production Order'    
        
    def __str__(self):
        return f"{self.docno}"

class ProductionComponent(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='production_components')
    docNo = models.PositiveIntegerField(default=1, unique=False)  
    
    code = models.CharField(max_length=20,default='',null=True)
    salesOrder= models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=100,default='',null=True)
    uom =  models.CharField(max_length=100,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    created = models.DateField(default=date.today, editable=True)
    
    def save(self, *args, **kwargs):
        if self.salesOrder:
            

            self.created = self.production.created
        if self.docNo:
            self.docNo = self.production.docno                          
        super().save(*args, **kwargs)   
    # def __str__(self):
    #     return self.name   
    
    
    
'''
  ____                         _           _       _____                                ____                       _                  _     _                 
 |  _ \    ___    ___    ___  (_)  _ __   | |_    |  ___|  _ __    ___    _ __ ___     |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __  
 | |_) |  / _ \  / __|  / _ \ | | | '_ \  | __|   | |_    | '__|  / _ \  | '_ ` _ \    | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \ 
 |  _ <  |  __/ | (__  |  __/ | | | |_) | | |_    |  _|   | |    | (_) | | | | | | |   |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |
 |_| \_\  \___|  \___|  \___| |_| | .__/   \__|   |_|     |_|     \___/  |_| |_| |_|   |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|
                                  |_|                                                                                                                         
'''

class ProductionReceipt(models.Model):
    docno = models.PositiveIntegerField(unique=True,default=1)
    created = models.DateField(default=date.today)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_DEFAULT,
        default=None,  # Set the default to None initially
    )   
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     
    class Meta:

        verbose_name = 'Receipt From Production'
        verbose_name_plural = 'Receipt From Production'   
        
        
    def save(self, *args, **kwargs):
        if not self.department_id:
            self.department = Department.objects.first()
        super().save(*args, **kwargs)
                 
    def __str__(self):
        return f"{self.docno}"


            
            
class ProductionReceiptItem(models.Model): 
    docNo = models.PositiveIntegerField(unique=False,default=1)    
   
    lineNo = models.CharField(max_length=4,default='0') # Add the lineNo field
    orderlineNo = models.CharField(max_length=4,default='0') # Add the lineNo field
    receiptNumber = models.ForeignKey(ProductionReceipt, on_delete=models.CASCADE, null=True, default=None)
    salesOrder = models.PositiveIntegerField(default=0)
    productionNo =  models.PositiveIntegerField(default=0)    
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    uom =  models.CharField(max_length=100,default='',null=True)    
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4,default=0,null=True)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,default=0,null=True)
    size = models.CharField(max_length=100,default='',null=True)  
    color = models.CharField(max_length=100,default='',null=True)  
    style = models.CharField(max_length=100,default='',null=True)   
    gweight = models.CharField(max_length=100,default='',null=True)    
    nweight = models.CharField(max_length=100,default='',null=True) 
    ctnno = models.CharField(max_length=100,default='',null=True)    
    remarks = models.CharField(max_length=100,default='') 
    department = models.CharField(max_length=50,default='1')
    created = models.DateField(default=date.today, editable=True)
    
    def save(self, *args, **kwargs):
        if self.receiptNumber:
            self.department = self.receiptNumber.department.name
            

            self.created = self.receiptNumber.created
        if self.docNo:
            self.docNo = self.receiptNumber.docno                       
        super().save(*args, **kwargs)    
     
    def __str__(self):
        return f": {self.docNo}"    

    @staticmethod
    def get_balance_report():
        # Calculate the total sum of SalesOrderItem.quantity for each code
        sales_order_totals = SalesOrderItem.objects.values('code').annotate(
            sales_total=Sum('quantity')
        )

        # Calculate the total sum of ProductionReceiptItem.quantity for each code grouped by department
        production_receipt_totals = ProductionReceiptItem.objects.values('code', 'department').annotate(
            production_total=Sum('quantity')
        )

        # Create a dictionary to store the balance report
        balance_report = {}

        # Calculate the balance for each code grouped by department
        for production_receipt in production_receipt_totals:
            code = production_receipt['code']
            department = production_receipt['department']
            production_total = production_receipt['production_total']
            
            sales_total = next(
                (item['sales_total'] for item in sales_order_totals if item['code'] == code),
                0
            )

            balance = sales_total - production_total

            if code not in balance_report:
                balance_report[code] = {}

            balance_report[code][department] = balance

        return balance_report    
    