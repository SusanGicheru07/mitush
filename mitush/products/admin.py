from django.contrib import admin
from .models import Category, Section, SubSection, Item, SectionItems

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_items')

    def get_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])
    get_items.short_description = 'Items'

    filter_vertical = ('items',)
    raw_id_fields = ('items',)
    search_fields = ('name',)

@admin.register(SubSection)
class SubSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'get_category')
    search_fields = ('name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'section':
            category_id = request.GET.get('category')
            if category_id:
                kwargs['queryset'] = Section.objects.filter(category_id=category_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_category(self, obj):
        return obj.section.category
    get_category.short_description = 'Category'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'section', 'subsection', 'name', 'price', 'stock')
    search_fields = ('name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'section':
            category_id = request.GET.get('category')
            if category_id:
                kwargs['queryset'] = Section.objects.filter(category_id=category_id)
        elif db_field.name == 'subsection':
            section_id = request.GET.get('section')
            if section_id:
                kwargs['queryset'] = SubSection.objects.filter(section_id=section_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(SectionItems)
class SectionItemsAdmin(admin.ModelAdmin):
    list_display = ('section', 'item', 'quantity')
    autocomplete_fields = ['section', 'item']
