from django.contrib import admin
from .models import StockIn

# Register your models here.
@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ['product', 'origin_price', 'sale_price', 'quantity', 'created']
    list_filter = ['product', 'created']