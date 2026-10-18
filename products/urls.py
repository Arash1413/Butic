from django.urls import path
from .views import product_list, product_detail
from django.urls import path, re_path 
from . import views

app_name = 'products'

urlpatterns = [   
    path('', product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    re_path(r'^(?P<slug>[-\w]+)/$', product_detail, name='product_detail'),
     path('favorite/toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('my-wishlist/', views.wishlist, name='wishlist'),
    
]