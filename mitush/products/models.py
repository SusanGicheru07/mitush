# products/models.py

from django.db import models
from django.urls import reverse
from django.db.models import Count
from random import sample

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'pk': self.pk})  # Changed from 'slug' to 'pk'
    
    def get_random_items(self, count=15):
        all_items = self.item_set.all()  # Using the reverse relationship
        
        if all_items.count() <= count:
            return all_items
        
        return sample(list(all_items), count)


class Section(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    items = models.ManyToManyField('Item', through='SectionItems', blank=True, related_name='sections')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('section-detail', kwargs={'slug': self.slug})

class SubSection(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subsections')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.section.name} - {self.name}"

class Item(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='items', default=1)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='item_section')
    subsection = models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name='item_subsection', null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True)
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.category.name}: {self.section.name} - {self.name}"

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'slug': self.slug})

    def get_price(self):
        return self.price

    @property
    def formatted_price(self):
        return f"Ksh{self.price:.2f}"

class SectionItems(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_sections')
    quantity = models.IntegerField()
