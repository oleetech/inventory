# accounting/models.py

from django.db import models

class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class ChartOfAccounts(models.Model):
    account_number = models.CharField(max_length=10, unique=True)
    account_name = models.CharField(max_length=100)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.account_number} - {self.account_name}"

class Transaction(models.Model):
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=4)
    transaction_type = models.CharField(max_length=10, choices=[('debit', 'Debit'), ('credit', 'Credit')])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.account} - {self.transaction_type} - {self.amount}"
    
    
class JournalEntry(models.Model):
    account = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=4)

    date = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.account} - {self.amount}"