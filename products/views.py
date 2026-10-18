from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from .models import Favorite
from django.http import JsonResponse 
from django.db.models import Q

def product_list(request, category_slug=None): 
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'products/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    return render(request, 'products/detail.html', {
        'product': product,
        'similar_products': similar_products
    })


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()
        status = 'removed'
    else:
        status = 'added'
    
    
    return JsonResponse({'status': status})
@login_required
def wishlist(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'products/wishlist.html', {'favorites': favorites})


def product_search(request):
    query = request.GET.get('q') 
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_available=True
        )
    return render(request, 'products/search_results.html', {
        'products': results,
        'query': query
    })