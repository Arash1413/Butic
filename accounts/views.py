from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Favorite  # این خط را اضافه کنید

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)
    # اضافه کردن لیست علاقه‌مندی‌ها
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    
    return render(request, 'accounts/dashboard.html', {
        'orders': orders,
        'favorites': favorites
    })