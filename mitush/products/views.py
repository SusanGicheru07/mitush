from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Item, Section, Category, SubSection
from cart.forms import AddToCartForm
from .forms import ItemForm

class ItemListView(ListView):
    model = Item
    template_name = 'products/category_page.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'products/product_detail.html'

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'products/item_form.html'
    success_url = reverse_lazy('item_list')

    def form_valid(self, form):
        item = form.save(commit=False)
        category_slug = self.request.POST.get('category')
        category = Category.objects.filter(slug=category_slug).first()
        item.section = Section.objects.filter(category=category).first()
        item.save()
        return super().form_valid(form)


def category_page(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    # Prefetch related sections, subsections, and items
    sections = Section.objects.filter(category=category).prefetch_related(
        Prefetch('subsections', queryset=SubSection.objects.prefetch_related(
            Prefetch('item_subsection', queryset=Item.objects.order_by('name'))
        ).order_by('name'))
    ).order_by('name')

    # Group items by subsection
    items_by_subsection = {}
    for section in sections:
        for subsection in section.subsections.all():
            items_by_subsection[subsection] = subsection.item_subsection.all()

    form = AddToCartForm()
    
    context = {
        'category': category,
        'sections': sections,
        'items_by_subsection': items_by_subsection,
        'form': form
    }
    
    return render(request, 'products/category_page.html', context)
