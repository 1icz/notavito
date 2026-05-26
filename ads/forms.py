from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'text', 'price', 'category', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }