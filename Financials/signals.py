from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from Financials.models import ChartOfAccounts, Transaction,JournalEntry
from Purchasing.models import PurchaseOrderInfo
from Sales.models import DeliveryInfo
@receiver(post_save, sender=PurchaseOrderInfo)
def create_purchase_order_transactions(sender, instance, created, **kwargs):
    if created:
        # Assuming "purchase_order" is the instance of PurchaseOrderInfo
        accounts_payable = ChartOfAccounts.objects.get(account_name="Accounts Payable")
        expense_account = ChartOfAccounts.objects.get(account_name="Office Supplies Expense")

        # Create a debit transaction for Accounts Payable
        debit_transaction = Transaction.objects.create(
            account=accounts_payable,
            amount=instance.totalAmount,
            transaction_type="debit"
        )

        # Create a credit transaction for the expense account
        credit_transaction = Transaction.objects.create(
            account=expense_account,
            amount=instance.totalAmount,
            transaction_type="credit"
        )

# Connect the signal handler to the PurchaseOrderInfo model
post_save.connect(create_purchase_order_transactions, sender=PurchaseOrderInfo)


@receiver(post_save, sender=DeliveryInfo)
def create_delivery_transactions(sender, instance, created, **kwargs):
    if created:
        # Assuming "delivery_info" is the instance of DeliveryInfo
        accounts_receivable = ChartOfAccounts.objects.get(account_name="Accounts Receivable")
        sales_revenue_account = ChartOfAccounts.objects.get(account_name="Sales Revenue")

        # Create a debit transaction for Accounts Receivable
        debit_transaction = Transaction.objects.create(
            account=accounts_receivable,
            amount=instance.totalAmount,
            transaction_type="debit"
        )

        # Create a credit transaction for the sales revenue account
        credit_transaction = Transaction.objects.create(
            account=sales_revenue_account,
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