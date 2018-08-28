from django.contrib import admin
from .models import Expenses, ExpenseType

# Register your models here.
@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ['name', 'month', 'amount', 'create_by']
    list_filter = ['name', 'month']