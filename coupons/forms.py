from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'input-text form-control', 'placeholder': 'Mã khuyến mãi'}
        )
    )
