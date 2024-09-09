from products.models import Category

def categories_processor(request):
    categories_with_sections = Category.objects.prefetch_related('sections').all()
    return {'categories_with_sections': categories_with_sections}
