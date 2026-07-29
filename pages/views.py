from django.shortcuts import render
from products.models import Category, Product
from django.db.models import Sum # این را حتما اضافه کنید

def home(request):
    # ۱. جدیدترین محصولات
    latest_products = Product.objects.all().order_by('-created_at')[:3]
    
    # ۲. دسته‌بندی‌ها
    categories = Category.objects.all()

    # ۳. پرفروش‌ترین محصولات (منطق جدید)
    # محصولاتی را پیدا کن که در سفارش‌های پرداخت‌شده (paid=True) هستند و تعدادشان را جمع بزن
    best_sellers = Product.objects.filter(order_items__order__paid=True)\
        .annotate(total_sold=Sum('order_items__quantity'))\
        .order_by('-total_sold')[:3]

    # نکته: اگر هنوز هیچ فروشی ندارید، برای اینکه صفحه خالی نماند، 
    # می‌توانید چند محصول تصادفی یا محبوب را نشان دهید:
    if not best_sellers:
        best_sellers = Product.objects.all().order_by('?')[:3]

    return render(request, 'pages/home.html', {
        'latest_products': latest_products,
        'categories': categories,
        'best_sellers': best_sellers, # این را به خروجی اضافه کردیم
    })