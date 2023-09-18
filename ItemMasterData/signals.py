from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Stock, ItemReceipt, ItemDelivery, IssueForProductionItem, LedgerEntry

@receiver(post_save, sender=Stock)
@receiver(post_save, sender=ItemReceipt)
@receiver(post_save, sender=ItemDelivery)
@receiver(post_save, sender=IssueForProductionItem)
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

        if transaction_type:
            ledger_entry = LedgerEntry(
                code=instance.code,
                name=instance.name,
                quantity=instance.quantity,
                created=instance.created,  # Modify this according to your data model
                transaction_type=transaction_type,
            )
            ledger_entry.save()

