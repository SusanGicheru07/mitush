# mitush/admin.py

from django.contrib import admin
from .cart.models import Cart, CartItem
from .products.models import Category, Section, Item, SectionItems

admin.site.register(Cart, admin.ModelAdmin)
admin.site.register(CartItem, admin.ModelAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Section, admin.ModelAdmin)
admin.site.register(Item, admin.ModelAdmin)
admin.site.register(SectionItems, admin.ModelAdmin)
