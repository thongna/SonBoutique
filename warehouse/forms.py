from .models import StockIn
from django import forms

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = ['product', 'origin_price', 'sale_price', 'quantity']