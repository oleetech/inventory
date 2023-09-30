from os import name
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from GeneralSettings.models import Unit,Department
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Add any other fields for the Warehouse model

    def __str__(self):
        return self.name

class ItemGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name
    
class Item(models.Model):
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    description = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.SET_DEFAULT, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item_group = models.ForeignKey(ItemGroup, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)

    class Meta:
    # Add any other fields you need
        verbose_name = 'Item Master Data'
        verbose_name_plural = 'Item Master Data'    
    def __str__(self):
        return self.name


class Stock(models.Model):
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateField(default=date.today, editable=True)    
    docNo = models.PositiveIntegerField(unique=False,default=1)    
    
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)     

class ItemReceiptinfo(models.Model):
    
    department = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default=None, blank=True)
    docno = models.PositiveIntegerField(default=1, unique=True)
    created = models.DateField(default=date.today, editable=True)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.department_id:
            self.department = Department.objects.first()
        super().save(*args, **kwargs)    
    class Meta:
    
        verbose_name = 'Goods Receipt'
        verbose_name_plural = 'Goods Receipt'
    def __str__(self):
        return " {}".format(self.docno)


class ItemReceipt(models.Model):
    item_info = models.ForeignKey(ItemReceiptinfo, on_delete=models.CASCADE, null=True, default=None)
    created = models.DateField(default=timezone.now)
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    
    department = models.CharField(max_length=50,default='1')    
    def save(self, *args, **kwargs):      
        if self.created:            
            self.created = self.item_info.created
        if self.department:            
            self.department = self.item_info.department.name            
                                      
        super().save(*args, **kwargs) 
        
    def __str__(self):
        return " {}".format(self.item_info.docno)

    def clean(self):
        if self.quantity == 0:
            raise ValidationError("Quantity cannot be 0.")


class ItemDeliveryinfo(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default=None, blank=True)
    
    docno = models.PositiveIntegerField(default=1, unique=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)  
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.department_id:
            self.department = Department.objects.first()
        super().save(*args, **kwargs)
    class Meta:
        
        verbose_name = 'Goods Delivery'
        verbose_name_plural = 'Goods Delivery'
    def __str__(self):
        return " {}".format(self.docno)


class ItemDelivery(models.Model):
    created = models.DateField(default=date.today, editable=True)
    item_info = models.ForeignKey(ItemDeliveryinfo, on_delete=models.CASCADE, null=True, default=None)
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    department = models.CharField(max_length=50,default='1')    
    def save(self, *args, **kwargs):      
        if self.created:            
            self.created = self.item_info.created
        if self.department:            
            self.department = self.item_info.department.name            
                                      
        super().save(*args, **kwargs)   
    def __str__(self):
        return f'{self.id}'
    
    

class IssueForProductionInfo(models.Model):
    docno = models.PositiveIntegerField(unique=True,default=1)
    created = models.DateField(default=date.today)

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_DEFAULT,
        default=None, blank=True  # Set the default to None initially
    )   
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     
    class Meta:

        verbose_name = ' Issue For Production'
        verbose_name_plural = 'Issue  For  Production'   
        
        
    def save(self, *args, **kwargs):
        if not self.department_id:
            self.department = Department.objects.first()
        super().save(*args, **kwargs)
                 
    def __str__(self):
        return f"{self.docno}"


            
            
class IssueForProductionItem(models.Model): 
    docNo = models.PositiveIntegerField(unique=False,default=1)    
    lineNo = models.CharField(max_length=4,default='0') # Add the lineNo field
    orderlineNo = models.CharField(max_length=4,default='0') # Add the lineNo field
    receiptNumber = models.ForeignKey(IssueForProductionInfo, on_delete=models.CASCADE, null=True, default=None)
    salesOrder = models.PositiveIntegerField(default=0)
    productionNo =  models.PositiveIntegerField(default=0)    
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)
    uom =  models.CharField(max_length=100,default='',null=True)    
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4,default=0,null=True)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,default=0,null=True)  
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
    
class LedgerEntry(models.Model):
    TRANSACTION_CHOICES = (
        ('STOCK', 'Stock'),
        ('ITEM_RECEIVED', 'Item Received'),
        ('ITEM_DELIVERY', 'Item Delivery'),
        ('ISSUE_FOR_PRODUCTION ', 'ISSUE FOR PRODUCTION'),      
        ('Goods_Receipt_Po_Item ', 'Purchase Goods received'),            
    )

    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    created = models.DateField(default=date.today, editable=True)
    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_CHOICES)
    docNo = models.PositiveIntegerField(unique=False,default=1)    
      

    
 