from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from .utils import send_otp
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
import random
from decimal import Decimal

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            otp_code = random.randint(100000, 999999)
            
            order_info = form.cleaned_data
            
            # ذخیره اطلاعات به صورت کاملا ساده و قابل فهم برای JSON
            request.session['order_info'] = {
                'first_name': order_info['first_name'],
                'last_name': order_info['last_name'],
                'phone': order_info['phone'],
                'address': order_info['address'],
                'city': order_info['city'],
                'postal_code': order_info['postal_code'],
                'total_price': cart.get_total_price(), # حالا این مقدار یک عدد صحیح (int) است
            }
            request.session['otp_code'] = otp_code
            
            mobile = order_info['phone']
            if send_otp(mobile, otp_code):
                return redirect('orders:verify_otp')
            else:
                form.add_error('phone', 'خطا در سامانه پیامکی.')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

def verify_otp(request):
    if request.method == 'POST':
        user_code = request.POST.get('otp')
        saved_code = request.session.get('otp_code')
        
        if str(user_code) == str(saved_code):
            # کد درست است! حالا سفارش را در دیتابیس ثبت می‌کنیم
            order_info = request.session.get('order_info')
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=order_info['first_name'],
                last_name=order_info['last_name'],
                phone=order_info['phone'],
                address=order_info['address'],
                city=order_info['city'],
                postal_code=order_info['postal_code'],
                # اگر فیلد هزینه کل دارید:
                # total_cost=Decimal(order_info['total_price']) 
            )
            
            cart = Cart(request)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            
            # پاک کردن سشن‌ها
            cart.clear()
            del request.session['otp_code']
            
            # هدایت به درگاه پرداخت (مرحله بعدی)
            request.session['order_id'] = order.id # ذخیره ID برای مرحله پرداخت
            return redirect('payment:process') 
        else:
            return render(request, 'orders/verify.html', {'error': 'کد وارد شده صحیح نیست.'})

    return render(request, 'orders/verify.html')