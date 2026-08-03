from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Favorite  
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # بلافاصله بعد ثبت‌نام وارد شود
            messages.success(request, "ثبت نام با موفقیت انجام شد.")
            return redirect('accounts:dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# ورود کاربر
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# خروج
def logout_user(request):
    logout(request)
    return redirect('pages:home')# این خط را اضافه کنید

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    # اضافه کردن لیست علاقه‌مندی‌ها
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    
    return render(request, 'accounts/dashboard.html', {
        'orders': orders,
        'favorites': favorites
    })