from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from Financials.models import ChartOfAccounts, Transaction,JournalEntry
from Purchasing.models import PurchaseOrderInfo,ApInvoiceInfo,GoodsReceiptPoInfo
from Sales.models import DeliveryInfo



# @receiver(post_save, sender=PurchaseOrderInfo)
# def create_purchase_order_transactions(sender, instance, created, **kwargs):
#     if created:
#         # Get the relevant accounts from your Chart of Accounts
#         debit_account = ChartOfAccounts.objects.get(account_name="Inventory")
#         credit_account = ChartOfAccounts.objects.get(account_name="Cash/Bank")

#         # Create a debit transaction for the Inventory account
#         debit_transaction = Transaction.objects.create(
#             account=debit_account,
#             amount=instance.totalAmount,
#             transaction_type="debit"
#         )

#         # Create a credit transaction for the Cash/Bank account
#         credit_transaction = Transaction.objects.create(
#             account=credit_account,
#             amount=instance.totalAmount,
#             transaction_type="credit"
#         )

# # Connect the signal handler to the PurchaseOrderInfo model
# post_save.connect(create_purchase_order_transactions, sender=PurchaseOrderInfo)
# # Signal handler for GoodsReceiptPoInfo
# @receiver(post_save, sender=GoodsReceiptPoInfo)
# def create_goods_receipt_transactions(sender, instance, created, **kwargs):
#     if created:
#         # Get the relevant accounts from your Chart of Accounts
#         debit_account = ChartOfAccounts.objects.get(account_name="Inventory")
        
#         credit_account = ChartOfAccounts.objects.get(account_name='Cost of Goods Sold (COGS)')

#         # Create a debit transaction for the Inventory account
#         debit_transaction = Transaction.objects.create(
#             account=debit_account,
#             amount=instance.totalAmount,
#             transaction_type="debit"
#         )

#         # Create a credit transaction for the dynamically determined credit account
#         credit_transaction = Transaction.objects.create(
#             account=credit_account,
#             amount=instance.totalAmount,
#             transaction_type="credit"
#         )

# # Connect the signal handler to the GoodsReceiptPoInfo model
# post_save.connect(create_goods_receipt_transactions, sender=GoodsReceiptPoInfo)


# @receiver(post_save, sender=ApInvoiceInfo)
# def create_ap_invoice_transactions(sender, instance, created, **kwargs):
#     if created:
#         # Get the relevant accounts from your Chart of Accounts
#         credit_account = ChartOfAccounts.objects.get(account_name="Cash/Bank")
#         debit_account = ChartOfAccounts.objects.get(account_name="Cost of Goods Sold (COGS)")  # Replace with the actual account name

#         # Create a credit transaction for the Accounts Payable account
#         credit_transaction = Transaction.objects.create(
#             account=credit_account,
#             amount=instance.totalAmount,
#             transaction_type="credit"
#         )

#         # Create a debit transaction for the specific account
#         debit_transaction = Transaction.objects.create(
#             account=debit_account,
#             amount=instance.totalAmount,
#             transaction_type="debit"
#         )

# # Connect the signal handler to the ApInvoiceInfo model
# post_save.connect(create_ap_invoice_transactions, sender=ApInvoiceInfo)


# @receiver(post_save, sender=DeliveryInfo)
# def create_delivery_transactions(sender, instance, created, **kwargs):
#     if created:
#         # Assuming "delivery_info" is the instance of DeliveryInfo
#         debit_account = ChartOfAccounts.objects.get(account_name="Accounts Receivable")
#         credit_account = ChartOfAccounts.objects.get(account_name="Sales Revenue")

#         # Create a debit transaction for Accounts Receivable
#         debit_transaction = Transaction.objects.create(
#             account=debit_account,
#             amount=instance.totalAmount,
#             transaction_type="debit"
#         )

#         # Create a credit transaction for the sales revenue account
#         credit_transaction = Transaction.objects.create(
#             account=credit_account,
#             amount=instance.totalAmount,
#             transaction_type="credit"
#         )

# # Connect the signal handler to the DeliveryInfo model
# post_save.connect(create_delivery_transactions, sender=DeliveryInfo)

@receiver(post_save, sender=JournalEntry)
def create_journal_transactions(sender, instance, **kwargs):
    if instance.account.account_name == 'Office Supplies Expense':
        # Create a credit Transaction for 'Office Supplies Expense'
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Office Supplies Expense'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )
        
        # Create a debit Transaction for 'Cash/Bank'
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )
    elif instance.account.account_name == "Owner's Equity":
        # Create a debit Transaction for 'Salaries and Wages'
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )
        
        # Create a credit Transaction for 'Cash/Bank'
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name="Owner's Equity"),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )
                
    elif instance.account.account_name == 'Salaries and Wages':
        # Create a debit Transaction for 'Salaries and Wages'
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Salaries and Wages'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )
        
        # Create a credit Transaction for 'Cash/Bank'
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )
    elif instance.account.account_name == 'Cash/Bank':
        # Create a debit Transaction for 'Cash/Bank'
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )
        

    elif instance.account.account_name == 'Accounts Receivable':
        # Create a debit Transaction for another account (e.g., Sales Revenue)
        # Replace 'Sales Revenue' with the appropriate revenue or income account
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Sales Revenue'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )
        
        # Create a credit Transaction for 'Accounts Receivable'
        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Accounts Receivable'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )                
        
    elif instance.account.account_name == 'Inventory':

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Inventory'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )          
        
    elif instance.account.account_name == 'Fixed Assets':

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Fixed Assets'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )     
        
    elif instance.account.account_name == 'Cost of Goods Sold (COGS)':

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Inventory'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )     
        
    elif instance.account.account_name == 'Rent Expense':

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Rent Expense'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )   
        
    elif instance.account.account_name == 'Utilities Expense':

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Utilities Expense'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )   
        
    elif instance.account.account_name == 'Other Income':

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Other Income'),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )   
        
    elif instance.account.account_name == "Owner's Equity":

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Cash/Bank'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name="Owner's Equity"),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )  
        
    elif instance.account.account_name == "Loans Payable":

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name='Loans Payable'),
            amount=instance.amount,
            transaction_type='debit',
            date=instance.date
        )

        Transaction.objects.create(
            account=ChartOfAccounts.objects.get(account_name="Cash/Bank"),
            amount=instance.amount,
            transaction_type='credit',
            date=instance.date
        )                                                
# Connect the signal handler to the DeliveryInfo model
post_save.connect(create_journal_transactions, sender=JournalEntry)