# accounting/admin.py

from django.contrib import admin
from .models import AccountType, ChartOfAccounts,Transaction,JournalEntry

class ChartOfAccountsAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'account_name', 'account_type', 'is_active')
    list_filter = ('account_type', 'is_active')
    search_fields = ('account_number', 'account_name')
    list_per_page = 20

admin.site.register(AccountType)
admin.site.register(ChartOfAccounts, ChartOfAccountsAdmin)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
