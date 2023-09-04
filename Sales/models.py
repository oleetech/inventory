from django.db import models
from django.utils import timezone
from BusinessPartners.models import BusinessPartner 
from ItemMasterData.models import Item
from datetime import date
from django.contrib.auth.models import User







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

    class Meta:

        verbose_name = 'Sales Order'
        verbose_name_plural = 'Sales Order'
        
    def __str__(self):
        return f"{self.docNo}"

class SalesOrderItem(models.Model):
    created = models.DateField(default=date.today, editable=True)
    order = models.ForeignKey(SalesOrderInfo, on_delete=models.CASCADE, null=True, default=None)    
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
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

    

        
        
    class Meta:

        verbose_name = ' Delivery'
        verbose_name_plural = 'Delivery '

    def __str__(self):
        return f" {self.docNo}"


class DeliveryItem(models.Model):    
    delivery = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    created = models.DateField(default=date.today, editable=True)
    orderNo = models.PositiveIntegerField(default=0)
    receiptNo =  models.PositiveIntegerField(default=0)
    lineNo =  models.PositiveIntegerField(default=0)       
    code = models.CharField(max_length=20,default='',null=True)
    name = models.CharField(max_length=100,default='',null=True)    
    uom = models.CharField(max_length=20,default='',null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4,default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    
    def save(self, *args, **kwargs):
        if self.created:


            self.created = self.delivery.created
                   
        super().save(*args, **kwargs)       
    def __str__(self):
        return f"{self.delivery}" 
    


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
    price = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    priceTotal = models.DecimalField(max_digits=10, decimal_places=4,null=True, blank=True, default=0)
    
    def save(self, *args, **kwargs):
        if self.created:


            self.created = self.order.created
                   
        super().save(*args, **kwargs)     
            
    def __str__(self):
        return f": {self.order}"          
    
    
    
    
    
    
    
    
    
   