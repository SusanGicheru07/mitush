from django.urls import path, include
from . import views

urlpatterns = [
    path('view/', views.view_cart, name='view_cart'),
    path('add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
    path('check-payment-status/<int:order_id>/', views.check_payment_status, name='check_payment_status'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),

]
