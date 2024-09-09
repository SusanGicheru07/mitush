from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Item
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from django.views.decorators.http import require_POST

import requests
import base64
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime




from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = []
    
    for cart_item in CartItem.objects.filter(cart=cart).select_related('item'):
        try:
            # Attempt to access the image URL
            image_url = cart_item.item.image.url if cart_item.item.image else None
        except ObjectDoesNotExist:
            # Handle case where the related Item object doesn't exist
            image_url = None
        except ValueError:
            # Handle case where image file is missing
            image_url = None
        
        subtotal = cart_item.item.price * cart_item.quantity
        cart_items.append({
            'cart_item': cart_item,
            'image_url': image_url,
            'subtotal': subtotal
        })
    
    total_items = sum(item['cart_item'].quantity for item in cart_items)
    total_price = sum(item['cart_item'].item.price * item['cart_item'].quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price,
    }
    
    return render(request, 'cart/cart.html', context)
   

@login_required
@require_POST
def add_to_cart(request, item_id):
    try:
        item = get_object_or_404(Item, id=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, item=item)
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        
        cart_items_count = sum(item.quantity for item in cart.cartitem_set.all())

        return JsonResponse({
            'success': True,
            'message': 'Item added to cart successfully',
            'cart_items_count': cart_items_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        for key, value in request.POST.items():
            if key.startswith('quantity-'):
                item_id = int(key.split('-')[1])
                try:
                    cart_item = CartItem.objects.get(id=item_id, cart=cart)
                    new_quantity = int(value)
                    if new_quantity > 0:
                        cart_item.quantity = new_quantity
                        cart_item.save()
                    else:
                        cart_item.delete()
                except CartItem.DoesNotExist:
                    pass  # Item not found, skip it
        cart.save()
    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cartitems.all().delete()
    return redirect('view_cart')

def generate_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    r = requests.get(api_URL, auth=(consumer_key, consumer_secret))
    
    return r.json()['access_token']


@login_required
def checkout_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        
        if not cart.items.exists():
            messages.warning(request, "Your cart is empty. Please add items before proceeding to checkout.")
            return redirect('home')
        
        delivery_methods = [
            {'value': 'pickup-star-mall', 'name': 'Pickup Point (Star Mall Along Tom Mboya Street Shop C2)', 'price': Decimal('0')},
            {'value': 'pickup-mtaani', 'name': 'Pickup Point near you (Pickup Mtaani Agent)', 'price': Decimal('150')},
            {'value': 'nationwide', 'name': 'Nationwide', 'price': Decimal('350')},
        ]

        # Get the selected delivery method, default to the first one
        selected_delivery = request.POST.get('delivery') or request.GET.get('delivery') or delivery_methods[0]['value']
        
        # Calculate shipping fee based on selected delivery method
        shipping_fee = next((method['price'] for method in delivery_methods if method['value'] == selected_delivery), Decimal('0'))

        subtotal = sum(item.subtotal for item in cart.items.all())
        grand_total = subtotal + shipping_fee

        if request.method == 'POST' and 'pay' in request.POST:
            # Process the final checkout form submission
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            county = request.POST.get('county')
            zip_code = request.POST.get('zip')
            delivery_method = request.POST.get('delivery')

            # Create a new order
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                county=county,
                zip_code=zip_code,
                delivery_method=delivery_method,
                total_amount=subtotal,
                shipping_fee=shipping_fee
            )

            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    item=cart_item.item,
                    quantity=cart_item.quantity,
                    price=cart_item.item.price
                )

            # Clear the cart
            cart.items.all().delete()
            cart.save()

            # Redirect to payment page or order confirmation
            return redirect('payment', order_id=order.id)

        context = {
            'cart_items': cart.items.all(),  # Use QuerySet instead of serialized data
            'subtotal': subtotal,
            'shipping_fee': shipping_fee,
            'grand_total': grand_total,
            'user': request.user,
            'delivery_methods': delivery_methods,
            'selected_delivery': selected_delivery,
        }
        
        return render(request, 'main/checkout.html', context)
    
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty. Please add items before proceeding to checkout.")
        return redirect('home')


@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.is_paid:
        messages.warning(request, "This order has already been paid for.")
        return redirect('order_confirmation', order_id=order.id)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        access_token = generate_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()).decode()
        
        request_data = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(order.total_amount + order.shipping_fee),
            "PartyA": phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourdomain.com/mpesa-callback/",
            "AccountReference": f"Order {order.id}",
            "TransactionDesc": "Payment for order" 
        }
        
        response = requests.post(api_url, json=request_data, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            order.mpesa_checkout_request_id = response_data['CheckoutRequestID']
            order.save()
            return JsonResponse({'success': True, 'message': 'STK push sent. Please complete the payment on your phone.'})
        else:
            return JsonResponse({'error': 'Failed to initiate M-Pesa payment'}, status=400)
    
    context = {
        'order': order,
    }
    return render(request, 'cart/payment.html', context)

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        
        if response['Body']['stkCallback']['ResultCode'] == 0:
            checkout_request_id = response['Body']['stkCallback']['CheckoutRequestID']
            order = Order.objects.get(mpesa_checkout_request_id=checkout_request_id)
            
            order.is_paid = True
            order.payment_date = timezone.now()
            order.payment_method = 'mpesa'
            order.save()
            
            send_mail(
                'Order Confirmation',
                f'Your order (ID: {order.id}) has been confirmed and paid for. Thank you for your purchase!',
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                fail_silently=False,
            )
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Payment failed'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def check_payment_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.is_paid:
        return JsonResponse({'status': 'paid'})
    else:
        return JsonResponse({'status': 'pending'})

@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'cart/order_confirmation.html', context)
