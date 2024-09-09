from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    
    def total_items(self, obj):
        return obj.total_items
    
    def total_price(self, obj):
        return obj.total_price

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item_name', 'item_price', 'quantity', 'subtotal', 'item_image')
    
    def item_name(self, obj):
        return obj.item.name
    
    def item_price(self, obj):
        return obj.item.price
    
    def subtotal(self, obj):
        return obj.subtotal
    
    def item_image(self, obj):
        if obj.item.image:  
            return "No Image"

    item_image.short_description = 'Image'
