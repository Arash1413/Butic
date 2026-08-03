from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='ایمیل')
    first_name = forms.CharField(max_length=100, label='نام')
    last_name = forms.CharField(max_length=100, label='نام خانوادگی')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']