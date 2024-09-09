from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import CategoryViewSet, SectionViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = router.urls
