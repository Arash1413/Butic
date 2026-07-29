from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name="تصویر دسته‌بندی")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name="نام لباس")
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField(verbose_name="توضیحات")
    price = models.IntegerField(verbose_name="قیمت (تومان)")
    discount_price = models.IntegerField(null=True, blank=True, verbose_name="قیمت با تخفیف")
    image = models.ImageField(upload_to='products/', verbose_name="تصویر اصلی")
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True, verbose_name="موجود در انبار")

    # سایزهای موجود (به صورت ساده)
    size_xs = models.BooleanField(default=False, verbose_name="XS")
    size_s = models.BooleanField(default=False, verbose_name="S")
    size_m = models.BooleanField(default=False, verbose_name="M")
    size_l = models.BooleanField(default=False, verbose_name="L")
    size_xl = models.BooleanField(default=False, verbose_name="XL")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

# برای گالری تصاویر (تصاویر بیشتر برای هر محصول)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')



class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # جلوگیری از تکراری شدن یک محصول برای یک کاربر

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"