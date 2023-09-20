from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Stock, ItemReceipt, ItemDelivery, IssueForProductionItem, LedgerEntry,Item
from Purchasing.models import GoodsReceiptPoItem
@receiver(post_save, sender=Stock)
@receiver(post_save, sender=ItemReceipt)
@receiver(post_save, sender=ItemDelivery)
@receiver(post_save, sender=IssueForProductionItem)
@receiver(post_save, sender=GoodsReceiptPoItem)
def create_ledger_entry(sender, instance, created, **kwargs):
    if created:
        transaction_type = None
        if sender == Stock:
            transaction_type = 'STOCK'
         
        elif sender == ItemReceipt:
            transaction_type = 'ITEM_RECEIVED'
        elif sender == ItemDelivery:
            transaction_type = 'ITEM_DELIVERY'
        elif sender == IssueForProductionItem:
            transaction_type = 'ISSUE_FOR_PRODUCTION'
        elif sender == GoodsReceiptPoItem:
            transaction_type = 'Goods_Receipt_Po_Item'            

        if transaction_type:
            ledger_entry = LedgerEntry(
                code=instance.code,
                name=instance.name,
                quantity=instance.quantity,
                created=instance.created,  # Modify this according to your data model
                transaction_type=transaction_type,
                
                
                
            )
            ledger_entry.save()

# @receiver(post_save, sender=Stock)
# def update_item_quantity(sender, instance, created, **kwargs):
#     if created:  # Only do this when a new Stock instance is created
#         item = Item.objects.filter(code=instance.code).first()
#         if item:
#             item.quantity = instance.quantity
#             item.save()