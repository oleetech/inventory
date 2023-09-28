from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from Financials.models import ChartOfAccounts, Transaction,JournalEntry
from Purchasing.models import PurchaseOrderInfo,ApInvoiceInfo,GoodsReceiptPoInfo
from Sales.models import DeliveryInfo



@receiver(post_save, sender=PurchaseOrderInfo)
def create_purchase_order_transactions(sender, instance, created, **kwargs):
    if created:
        # Get the relevant accounts from your Chart of Accounts
        debit_account = ChartOfAccounts.objects.get(account_name="Inventory")
        credit_account = ChartOfAccounts.objects.get(account_name="Cash/Bank")

        # Create a debit transaction for the Inventory account
        debit_transaction = Transaction.objects.create(
            account=debit_account,
            amount=instance.totalAmount,
            transaction_type="debit"
        )

        # Create a credit transaction for the Cash/Bank account
        credit_transaction = Transaction.objects.create(
            account=credit_account,
            amount=instance.totalAmount,
            transaction_type="credit"
        )

# Connect the signal handler to the PurchaseOrderInfo model
post_save.connect(create_purchase_order_transactions, sender=PurchaseOrderInfo)
# Signal handler for GoodsReceiptPoInfo
@receiver(post_save, sender=GoodsReceiptPoInfo)
def create_goods_receipt_transactions(sender, instance, created, **kwargs):
    if created:
        # Get the relevant accounts from your Chart of Accounts
        debit_account = ChartOfAccounts.objects.get(account_name="Inventory")
        
        credit_account = ChartOfAccounts.objects.get(account_name='Cost of Goods Sold (COGS)')

        # Create a debit transaction for the Inventory account
        debit_transaction = Transaction.objects.create(
            account=debit_account,
            amount=instance.totalAmount,
            transaction_type="debit"
        )

        # Create a credit transaction for the dynamically determined credit account
        credit_transaction = Transaction.objects.create(
            account=credit_account,
            amount=instance.totalAmount,
            transaction_type="credit"
        )

# Connect the signal handler to the GoodsReceiptPoInfo model
post_save.connect(create_goods_receipt_transactions, sender=GoodsReceiptPoInfo)


@receiver(post_save, sender=ApInvoiceInfo)
def create_ap_invoice_transactions(sender, instance, created, **kwargs):
    if created:
        # Get the relevant accounts from your Chart of Accounts
        credit_account = ChartOfAccounts.objects.get(account_name="Accounts Payable")
        debit_account = ChartOfAccounts.objects.get(account_name="Cost of Goods Sold (COGS)")  # Replace with the actual account name

        # Create a credit transaction for the Accounts Payable account
        credit_transaction = Transaction.objects.create(
            account=credit_account,
            amount=instance.totalAmount,
            transaction_type="credit"
        )

        # Create a debit transaction for the specific account
        debit_transaction = Transaction.objects.create(
            account=debit_account,
            amount=instance.totalAmount,
            transaction_type="debit"
        )

# Connect the signal handler to the ApInvoiceInfo model
post_save.connect(create_ap_invoice_transactions, sender=ApInvoiceInfo)


@receiver(post_save, sender=DeliveryInfo)
def create_delivery_transactions(sender, instance, created, **kwargs):
    if created:
        # Assuming "delivery_info" is the instance of DeliveryInfo
        debit_account = ChartOfAccounts.objects.get(account_name="Accounts Receivable")
        credit_account = ChartOfAccounts.objects.get(account_name="Sales Revenue")

        # Create a debit transaction for Accounts Receivable
        debit_transaction = Transaction.objects.create(
            account=debit_account,
            amount=instance.totalAmount,
            transaction_type="debit"
        )

        # Create a credit transaction for the sales revenue account
        credit_transaction = Transaction.objects.create(
            account=credit_account,
            amount=instance.totalAmount,
            transaction_type="credit"
        )

# Connect the signal handler to the DeliveryInfo model
post_save.connect(create_delivery_transactions, sender=DeliveryInfo)

@receiver(post_save, sender=JournalEntry)
def create_journal_transactions(sender, instance, created, **kwargs):
    if created:

        # Create a credit transaction for the sales revenue account
        credit_transaction = Transaction.objects.create(
            account=instance.account,
            amount=instance.amount,
            transaction_type=instance.transaction_type,
        )

# Connect the signal handler to the DeliveryInfo model
post_save.connect(create_journal_transactions, sender=JournalEntry)