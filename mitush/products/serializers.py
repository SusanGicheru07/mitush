# products/serializers.py

from rest_framework import serializers
from .models import Item, Section, Category

class CategorySerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'sections']

    def get_sections(self, obj):
        return SectionSerializer(obj.sections.all(), many=True).data

class SectionSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'category', 'items']

    def get_items(self, obj):
        return ItemSerializer(obj.items.all(), many=True).data

class ItemSerializer(serializers.ModelSerializer):
    section = SectionSerializer(read_only=True)
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'section', 'name', 'description', 'price', 'formatted_price', 'image', 'stock', 'slug']

    def get_formatted_price(self, obj):
        return f"Ksh{obj.price:.2f}"

class ProductSerializer(ItemSerializer):
    pass
