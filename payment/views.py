
import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.http import HttpResponse

# این کد (PIN) را از پنل آقای پرداخت بخش درگاه‌ها دریافت کنید
PIN = "07CB55632240088D0504" 

def payment_process(request):
    # گرفتن سفارش از سشن (که در مرحله قبل ساختیم)
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    amount = order.get_total_cost() # مبلغ به تومان
    callback_url = "http://127.0.0.1:8000/payment/callback/" # آدرس برگشت

    # مرحله اول: درخواست تراکنش
    url = "https://panel.aqayepardakht.ir/api/v2/create"
    data = {
        "pin": PIN,
        "amount": amount,
        "callback": callback_url,
        "invoice_id": str(order.id),
        "description": f"پرداخت سفارش شماره {order.id}"
    }

    try:
        response = requests.post(url, data=data)
        result = response.json()
        
        if result['status'] == "success":
            # ذخیره کد تراکنش برای مرحله تایید
            order.tracking_code = result['transid'] 
            order.save()
            # هدایت کاربر به درگاه بانک
            return redirect(f"https://panel.aqayepardakht.ir/startpay/{result['transid']}")
        else:
            return HttpResponse(f"خطا در ایجاد تراکنش: {result['code']}")
    except Exception as e:
        return HttpResponse(f"خطا در اتصال به درگاه: {e}")

def payment_callback(request):
    # اطلاعاتی که آقای پرداخت برای ما برمی‌گرداند
    status = request.POST.get('status')
    transid = request.POST.get('transid')
    
    if status == "1": # یعنی پرداخت اولیه موفق بوده
        order = get_object_or_404(Order, tracking_code=transid)
        
        # مرحله دوم: تایید نهایی تراکنش (Verify)
        url = "https://panel.aqayepardakht.ir/api/v2/verify"
        data = {
            "pin": PIN,
            "amount": order.get_total_cost(),
            "transid": transid
        }
        
        response = requests.post(url, data=data)
        result = response.json()
        
        if result['status'] == "success":
            # پرداخت ۱۰۰٪ تایید شد!
            order.paid = True
            order.save()
            return render(request, 'payment/success.html', {'order': order})
        else:
            return render(request, 'payment/failed.html', {'error': result['code']})
    
    return render(request, 'payment/failed.html', {'error': 'تراکنش توسط کاربر لغو شد.'})

# Create your views here.
