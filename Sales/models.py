from django.db import models
from django.utils import timezone
from BusinessPartners.models import BusinessPartner 
from ItemMasterData.models import Item
from datetime import date
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django import forms







class SalesEmployee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateField()
    active = models.BooleanField(default=False)  # New field for active status

    # You can add more fields as needed, such as address, manager, etc.

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 


'''
  ____            _                   ___               _               
 / ___|    __ _  | |   ___   ___     / _ \   _ __    __| |   ___   _ __ 
 \___ \   / _` | | |  / _ \ / __|   | | | | | '__|  / _` |  / _ \ | '__|
  ___) | | (_| | | | |  __/ \__ \   | |_| | | |    | (_| | |  __/ | |   
 |____/   \__,_| |_|  \___| |___/    \___/  |_|     \__,_|  \___| |_|   
                                                                        
'''
# Create your models here.
class SalesOrderInfo(models.Model):
    Status_CHOICES = [
        ('O', 'Open'),
        ('H', 'Hold'),
        ('C', 'Close'),
        ('F', 'Canceled')
        
    ] 
    status = models.CharField(max_length=1, choices=Status_CHOICES,default='O')       
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.CASCADE, default=1)  # Set the default to an existing SalesEmployee or a specific ID
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    remarks = models.CharField(max_length=250,default='',blank=True)
    edd = models.DateField(default=timezone.now)

    class Meta:

        verbose_name = 'Sales Order'
        verbose_name_plural = 'Sales Order'
        
    def __str__(self):
        return f"{self.docNo}"

class SalesOrderItem(models.Model):
    created = models.DateField(default=date.today, editable=True)
    order = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE, null=True, default=None) 
    docNo = models.PositiveIntegerField(default=1, unique=False)  
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    description = models.CharField(max_length=255,default='',null=True,blank=True)    

    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    size = models.CharField(max_length=100,default='',null=True,blank=True)  
    color = models.CharField(max_length=100,default='',null=True,blank=True)  
    style = models.CharField(max_length=250,default='',null=True,blank=True)   
    po = models.CharField(max_length=250,default='',null=True,blank=True)       
    gweight = models.CharField(max_length=100,default='',null=True,blank=True)    
    nweight = models.CharField(max_length=100,default='',null=True,blank=True) 
    ctnno = models.CharField(max_length=100,default='',null=True,blank=True)                       
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    lineNo = models.PositiveIntegerField(default=1)  # Add the lineNo field
   
    def save(self, *args, **kwargs):
        if self.created:
            self.created = self.order.created
        if self.docNo:
            self.docNo = self.order.docNo            
                   
        super().save(*args, **kwargs)   
            
    def __str__(self):
        return f": {self.order}"
    
    
'''
  ____           _   _                               
 |  _ \    ___  | | (_) __   __   ___   _ __   _   _ 
 | | | |  / _ \ | | | | \ \ / /  / _ \ | '__| | | | |
 | |_| | |  __/ | | | |  \ V /  |  __/ | |    | |_| |
 |____/   \___| |_| |_|   \_/    \___| |_|     \__, |
                                               |___/ 
'''

class DeliveryInfo(models.Model):
    Status_CHOICES = [
        ('O', 'Open'),
        ('H', 'Hold'),
        ('C', 'Close'),
        ('F', 'Canceled')
        
    ] 
    status = models.CharField(max_length=1, choices=Status_CHOICES,default='O')      
    docNo = models.PositiveIntegerField(unique=True,default=1)    
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateTimeField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.CASCADE, default=1)  # Set the default to an existing SalesEmployee or a specific ID
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    salesOrder = models.PositiveIntegerField(default=0)
 
    delivertobuyerdate = models.DateField(default=None, blank=True, null=True)
    challanreceiveddate = models.DateField(default=None, blank=True, null=True)

        
        
    class Meta:

        verbose_name = ' Delivery'
        verbose_name_plural = 'Delivery '

    def __str__(self):
        return f" {self.docNo}"
    
    
class DeliveryItem(models.Model):   
    docNo = models.PositiveIntegerField(unique=False,default=1)    
    delivery = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    created = models.DateField(default=date.today, editable=True)
    orderNo = models.PositiveIntegerField(default=0)    
    receiptNo =  models.PositiveIntegerField(default=0)
    lineNo =  models.PositiveIntegerField(default=0) 
    orderlineNo = models.CharField(max_length=4,default='0') # Add the lineNo field          
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    size = models.CharField(max_length=100,default='',null=True)  
    color = models.CharField(max_length=100,default='',null=True)  
    style = models.CharField(max_length=100,default='',null=True)   
    gweight = models.CharField(max_length=100,default='',null=True)    
    nweight = models.CharField(max_length=100,default='',null=True) 
    ctnno = models.CharField(max_length=100,default='',null=True)       
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    
    def save(self, *args, **kwargs):
        if self.created:
            self.created = self.delivery.created
        if self.docNo:
            self.docNo = self.delivery.docNo    
                   
        super().save(*args, **kwargs)       
    def __str__(self):
        return f"{self.delivery}"     
class AdditionalDeliveryData(models.Model):
    delivery_info = models.OneToOneField(DeliveryInfo, on_delete=models.CASCADE,unique=True)
    delivertobuyerdate = models.DateField(default=date.today, editable=True)

    def __str__(self):
        return f"{self.delivery_info.docNo}"

    def save(self, *args, **kwargs):
        # Update the delivertobuyerdate of the associated DeliveryInfo
        self.delivery_info.delivertobuyerdate = self.delivertobuyerdate
        self.delivery_info.save()
        super().save(*args, **kwargs)
        
    class Meta:

        verbose_name = ' Challan Pass From Gate '
        verbose_name_plural = 'Challan Pass From Gate '
        
        
class ChallanReceivedDeliveryData(models.Model):
    delivery_info = models.OneToOneField(DeliveryInfo, on_delete=models.CASCADE,unique=True)
    challanreceiveddate = models.DateField(default=date.today, editable=True)

    def __str__(self):
        return f"{self.delivery_info.docNo}"

    def save(self, *args, **kwargs):
        # Update the delivertobuyerdate of the associated DeliveryInfo
        self.delivery_info.challanreceiveddate = self.challanreceiveddate
        self.delivery_info.save()
        super().save(*args, **kwargs)
        
    class Meta:

        verbose_name = '  Received Challan From Customer '
        verbose_name_plural = 'Received Challan From Customer '
                
        


    


'''
  ____            _                   ___                    _            _     _                 
 / ___|    __ _  | |   ___   ___     / _ \   _   _    ___   | |_    ___  | |_  (_)   ___    _ __  
 \___ \   / _` | | |  / _ \ / __|   | | | | | | | |  / _ \  | __|  / _ \ | __| | |  / _ \  | '_ \ 
  ___) | | (_| | | | |  __/ \__ \   | |_| | | |_| | | (_) | | |_  |  __/ | |_  | | | (_) | | | | |
 |____/   \__,_| |_|  \___| |___/    \__\_\  \__,_|  \___/   \__|  \___|  \__| |_|  \___/  |_| |_|
                                                                                                  
'''    
class SalesQuotetionInfo(models.Model):
    Status_CHOICES = [
        ('O', 'Open'),
        ('H', 'Hold'),
        ('C', 'Close'),
        ('F', 'Canceled')
        
    ] 
    status = models.CharField(max_length=1, choices=Status_CHOICES,default='O')      
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.CASCADE, default=1)  # Set the default to an existing SalesEmployee or a specific ID
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:

        verbose_name = 'Sales Quotetion'
        verbose_name_plural = 'Sales Quotetion'
        
    def __str__(self):
        return f"{self.docNo}"   
    

class SalesQuotetionItem(models.Model):
    created = models.DateField(default=date.today, editable=True)
    order = models.ForeignKey(SalesQuotetionInfo, on_delete=models.CASCADE, null=True, default=None)    
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
    size = models.CharField(max_length=100,default='',null=True)  
    color = models.CharField(max_length=100,default='',null=True)  
    style = models.CharField(max_length=100,default='',null=True)   
    gweight = models.CharField(max_length=100,default='',null=True)    
    nweight = models.CharField(max_length=100,default='',null=True) 
    ctnno = models.CharField(max_length=100,default='',null=True)       
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    
    def save(self, *args, **kwargs):
        if self.created:


            self.created = self.order.created
                   
        super().save(*args, **kwargs)       
    def __str__(self):
        return f": {self.order}"


'''
  ____           _                          
 |  _ \    ___  | |_   _   _   _ __   _ __  
 | |_) |  / _ \ | __| | | | | | '__| | '_ \ 
 |  _ <  |  __/ | |_  | |_| | | |    | | | |
 |_| \_\  \___|  \__|  \__,_| |_|    |_| |_|
                                            

                                                                                                  
'''    
class ReturnInfo(models.Model):
    Status_CHOICES = [
        ('O', 'Open'),
        ('H', 'Hold'),
        ('C', 'Close'),
        ('F', 'Canceled')
        
    ] 
    status = models.CharField(max_length=1, choices=Status_CHOICES,default='O')      
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.CASCADE, default=1)  # Set the default to an existing SalesEmployee or a specific ID
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:

        verbose_name = 'Return'
        verbose_name_plural = 'Return'
        
    def __str__(self):
        return f"{self.docNo}"   
    

class ReturnItem(models.Model):
    created = models.DateField(default=date.today, editable=True)
    order = models.ForeignKey(ReturnInfo, on_delete=models.CASCADE, null=True, default=None)    
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    size = models.CharField(max_length=100,default='',null=True)  
    color = models.CharField(max_length=100,default='',null=True)  
    style = models.CharField(max_length=100,default='',null=True)   
    gweight = models.CharField(max_length=100,default='',null=True)    
    nweight = models.CharField(max_length=100,default='',null=True) 
    ctnno = models.CharField(max_length=100,default='',null=True)       
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    
    def save(self, *args, **kwargs):
        if self.created:


            self.created = self.order.created
                   
        super().save(*args, **kwargs)      
    def __str__(self):
        return f": {self.order}"      
    
    
    
class ARInvoiceInfo(models.Model):
    Status_CHOICES = [
        ('O', 'Open'),
        ('H', 'Hold'),
        ('C', 'Close'),
        ('F', 'Canceled')
        
    ] 
    status = models.CharField(max_length=1, choices=Status_CHOICES,default='O')      
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.CASCADE, default=1)  # Set the default to an existing SalesEmployee or a specific ID
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    salesOrder = models.PositiveIntegerField(default=0)
    deliveryNo = models.PositiveIntegerField(default=0,unique=True)

    class Meta:

        verbose_name = 'AR Invoice'
        verbose_name_plural = 'AR Invoice'
        
    def __str__(self):
        return f"{self.docNo}"   
    

class ARInvoiceItem(models.Model):
    created = models.DateField(default=date.today, editable=True)
    order = models.ForeignKey(ARInvoiceInfo, on_delete=models.CASCADE, null=True, default=None)    
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    size = models.CharField(max_length=100,default='',null=True)  
    color = models.CharField(max_length=100,default='',null=True)  
    style = models.CharField(max_length=100,default='',null=True)   
    gweight = models.CharField(max_length=100,default='',null=True)    
    nweight = models.CharField(max_length=100,default='',null=True) 
    ctnno = models.CharField(max_length=100,default='',null=True)       
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    deliveryNo =  models.PositiveIntegerField(default=0)
    deliverylineNo = models.PositiveIntegerField(default=0)       
    lineNo =  models.PositiveIntegerField(default=0) 
    orderNo = models.PositiveIntegerField(default=0)    
    
    def save(self, *args, **kwargs):
        if self.created:


            self.created = self.order.created
            self.deliveryNo = self.order.deliveryNo       
            self.orderNo = self.order.salesOrder                          
        super().save(*args, **kwargs)     
            
    def __str__(self):
        return f": {self.id}"          
    
    
class CustomerComplaint(models.Model):
    docNo = models.PositiveIntegerField(default=1, unique=True)    
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    salesOrder = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE)
    deliveryNo = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE,default=None,blank=True)
    created = models.DateField(default=date.today, editable=True)
    description = models.TextField() # Change This Line
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('resolved', 'Resolved')])    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:

        verbose_name = 'Customer Complain '
        verbose_name_plural = 'Customer Complain'    
    def __str__(self):
        return f" {self.docNo}"      
class CustomerComplaintItem(models.Model):
    created = models.DateField(default=date.today, editable=True)
    order = models.ForeignKey(CustomerComplaint, on_delete=models.CASCADE, null=True, default=None)    
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)  
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)         
    solution = models.CharField(max_length=100,default='',null=True)  
    symptom = models.CharField(max_length=100,default='',null=True)    
    
    
   