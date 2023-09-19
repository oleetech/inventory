from .models import Warehouse, ItemGroup,Item, Stock, ItemReceiptinfo, ItemReceipt, ItemDeliveryinfo, ItemDelivery,IssueForProductionInfo,IssueForProductionItem,LedgerEntry
from Purchasing.models import GoodsReceiptPoItem,GoodsReturnItem,PurchaseItem
from Production.models import Production,ProductionComponent
from Sales.models import SalesOrderItem,DeliveryItem
from django.db import models
def calculate_instock(code):
    stock_quantity = Stock.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    receipt_quantity = ItemReceipt.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    delivery_quantity = ItemDelivery.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    purchase_order_goods_receipt = GoodsReceiptPoItem.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    purchase_order_goods_return = GoodsReturnItem.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    issue_for_production= IssueForProductionItem.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    instock = stock_quantity + purchase_order_goods_receipt + receipt_quantity - delivery_quantity - purchase_order_goods_return - issue_for_production
    return instock