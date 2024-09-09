from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from main.forms import UserRegistrationForm
from django.urls import reverse_lazy
from products.models import Item, Category, SubSection, SectionItems
from cart.models import Cart, CartItem

from django.db.models import Prefetch


def home(request):
     categories = Category.objects.all()
     categories_with_items = Category.objects.prefetch_related(
        Prefetch('items', queryset=Item.objects.order_by('?')[:15], to_attr='random_items')
     )
     context = {
        'categories_with_items': categories_with_items,
        'categories': categories,
        'csrf_token': get_token(request),
     }
     return render(request, 'main/index.html', context)

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
    
    next_url = request.GET.get('next', '')
    return render(request, 'main/login.html', {'next': next_url})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    next_url = request.GET.get('next', '')
    return render(request, 'main/login.html', {'form': form, 'next': next_url})



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            f'New contact form submission from {name}',
            f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}',
            email,
            ['susangicheru07@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent. Thank you!')
        return redirect('home')
    
    return redirect('home')
        
