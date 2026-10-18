
import requests
import json
from django.shortcuts import render, redirect, get_object_or_404, reverse
from config import settings
from orders.models import Order
from django.http import HttpResponse

# این کد (PIN) را از پنل آقای پرداخت بخش درگاه‌ها دریافت کنید


def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # مبلغ باید عدد صحیح و به تومان باشد (بین ۱,۰۰۰ تا ۴۰۰,۰۰۰,۰۰۰)
    amount = int(order.get_total_cost()) 
    
    # ساخت آدرس بازگشتی به صورت خودکار
    callback_url = request.build_absolute_uri(reverse('payment:callback'))
    
    # مرحله اول: ایجاد تراکنش (Create)
    url = "https://panel.aqayepardakht.ir/api/v2/create"
    payload = {
        'pin': settings.AQAYEPARDAKHT_PIN, # برای تست بنویسید 'sandbox'  
        'amount': amount,
        'callback': callback_url,
        'mobile': order.phone,
        'description': f'پرداخت سفارش شماره {order.id}',
    }
    
    try:
        response = requests.post(url, data=payload)
        result = response.json()
        
        if result['status'] == 'success':
            trans_id = result['transid']
            request.session['order_id'] = order.id
            
            # مرحله دوم: انتقال به درگاه
            # اگر پین 'sandbox' است، آدرس متفاوت است
            if settings.AQAYEPARDAKHT_PIN == 'sandbox':
                return redirect(f'https://panel.aqayepardakht.ir/startpay/sandbox/{trans_id}')
            else:
                return redirect(f'https://panel.aqayepardakht.ir/startpay/{trans_id}')
        else:
            # نمایش کد خطا (مثلا -15)
            return render(request, 'payment/error.html', {'error': result['code']})
    except Exception as e:
        return render(request, 'payment/error.html', {'error': 'خطا در ارتباط با سرور درگاه'})

def payment_callback(request):
    # مرحله سوم: بازگشت از درگاه (آقای پرداخت داده‌ها را POST می‌کند)
    # برای اطمینان هم POST و هم GET را چک می‌کنیم
    data = request.POST if request.method == 'POST' else request.GET
    
    status = data.get('status')
    trans_id = data.get('transid')
    order_id = request.session.get('order_id')
    
    if not order_id:
        return render(request, 'payment/fail.html', {'error': 'سفارش یافت نشد'})
        
    order = get_object_or_404(Order, id=order_id)
    
    # اگر وضعیت ۱ بود یعنی پرداخت در بانک موفق بوده، حالا باید تایید (Verify) کنیم
    if status == '1':
        # مرحله چهارم: وریفای تراکنش
        verify_url = "https://panel.aqayepardakht.ir/api/v2/verify"
        verify_payload = {
            'pin': settings.AQAYEPARDAKHT_PIN, 
            'amount': int(order.get_total_cost()),
            'transid': trans_id
        }
        
        try:
            verify_res = requests.post(verify_url, data=verify_payload).json()
            
            if verify_res['status'] == 'success':
                # پرداخت ۱۰۰٪ تایید شد
                order.paid = True
                order.save()
                # پاک کردن سبد خرید و اطلاعات موقت
                if 'order_id' in request.session:
                    del request.session['order_id']
                return render(request, 'payment/success.html', {'order': order})
            else:
                return render(request, 'payment/fail.html', {'error': 'تاییدیه درگاه دریافت نشد'})
        except:
            return render(request, 'payment/fail.html', {'error': 'خطا در عملیات وریفای'})
            
    return render(request, 'payment/fail.html', {'error': 'پرداخت توسط کاربر لغو شد'})