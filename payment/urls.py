from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='process'), 
    path('callback/', views.payment_callback, name='callback'),
]