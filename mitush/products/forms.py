from django import forms
from .models import Item, Section

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'image', 'stock']
        widgets = {
            'section': forms.Select(attrs={'id': 'category'}),
        }
