from .models import Messages
from django import forms

class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['title', 'body', 'name', 'phone_number', 'email']

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Tiêu đề*'}
        )
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Số điện thoại*'}
        )
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Tên*'}
        )
    )