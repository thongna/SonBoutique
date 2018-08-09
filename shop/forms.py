from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Tên*'}
        )
    )

