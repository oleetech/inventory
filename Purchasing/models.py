from django.db import models
from django.utils import timezone
from BusinessPartners.models import BusinessPartner 
from ItemMasterData.models import Item
from datetime import date


class PurchaseOrderInfo(models.Model):
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)

    class Meta:

        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Order'
        
    def __str__(self):
        return f"{self.docNo}"

class PurchaseItem(models.Model):
    created = models.DateField(default=date.today, editable=True)    
    order = models.ForeignKey(PurchaseOrderInfo, on_delete=models.CASCADE, null=True, default=None)    
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
    
    
    
class GoodsReceiptPoInfo(models.Model):
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)

    class Meta:

        verbose_name = 'Goods Receipt Po'
        verbose_name_plural = 'Goods Receipt Po'
        
    def __str__(self):
        return f"{self.docNo}"   
    

class GoodsReceiptPoItem(models.Model):
    created = models.DateField(default=date.today, editable=True)        
    order = models.ForeignKey(GoodsReceiptPoInfo, on_delete=models.CASCADE, null=True, default=None)    
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




class GoodsReturnInfo(models.Model):
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)

    class Meta:

        verbose_name = 'Goods Return'
        verbose_name_plural = 'Goods Return'
        
    def __str__(self):
        return f"{self.docNo}"   
    

class GoodsReturnItem(models.Model):
    created = models.DateField(default=date.today, editable=True)            
    order = models.ForeignKey(GoodsReturnInfo, on_delete=models.CASCADE, null=True, default=None)    
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
    
    
    
class ApInvoiceInfo(models.Model):
    docNo = models.PositiveIntegerField(default=1, unique=True)
    customerName = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE, null=True, default=None)
    address = models.CharField(max_length=250,blank=True)
    created = models.DateField(default=timezone.now)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True,default=0)
    totalQty = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)

    class Meta:

        verbose_name = 'Ap Invoice'
        verbose_name_plural = 'Ap Invoice'
        
    def __str__(self):
        return f"{self.docNo}"   
    

class ApInvoiceItem(models.Model):
    created = models.DateField(default=date.today, editable=True)                
    order = models.ForeignKey(ApInvoiceInfo, on_delete=models.CASCADE, null=True, default=None)    
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