from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemListView, ItemDetailView, ItemCreateView, category_page
from .api import urlpatterns as api_urls
from . import views

urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('create/', ItemCreateView.as_view(), name='item_create'),
    path('category/<int:category_id>/', views.category_page, name='category_page'),

] + api_urls
