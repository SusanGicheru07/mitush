from django import forms
from .models import CartItem

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'
        exclude = [] 
