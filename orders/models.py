from django.db import models
from products.models import Product
from django.conf import settings

class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    phone = models.CharField(max_length=11, verbose_name="شماره موبایل")
    address = models.TextField(verbose_name="آدرس دقیق")
    city = models.CharField(max_length=50, verbose_name="شهر")
    postal_code = models.CharField(max_length=10, verbose_name="کد پستی")
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"

    def __str__(self):
        return f'سفارش {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity