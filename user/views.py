from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from django.contrib.auth.decorators import login_required

from electric.utils import menu
from shop.models import Customer, Cart, Notification, Order, Shop
from .forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.


def profile(request):
    # --profile-----------------------------------------------------------------------------------
    customers = Customer.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=customers, in_order=False).first()
    customer_count = Customer.objects.get(user=request.user)
    notifications = Notification.objects.all(customer_count)
    shop = Shop.objects.all()
    shop_count = shop.count()
    order = Order.objects.all()
    order_count = order.count()
    context = {
        'shop_count': shop_count,
        'order_count': order_count,
        'menu': menu,
        'cart': cart,
        'notifications': notifications,
        'customer_count': customer_count,
    }
    return render(request, 'user/profile.html', context)


def profile_update(request):
    # -profile_update------------------------------------------------------------------------------
    customers = Customer.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=customers, in_order=False).first()
    customer_count = Customer.objects.get(user=request.user)
    notifications = Notification.objects.all(customer_count)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'menu': menu,
        'cart': cart,
        'notifications': notifications,
        'customer_count': customer_count,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user/profile_update.html', context)