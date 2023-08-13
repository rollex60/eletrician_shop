from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, UpdateView
from flask.json import tag
from django.contrib.auth import models
from .decorators import allowed_users
from .forms import LoginForm, RegistrationForm, User, ProductForm, ProductEditForm, NotificationForm, RegistrationUserForm
from django.shortcuts import render, redirect
from django import views
from electric.mixins import CartMixin, NotificationsMixin, TagMixin
from electric.utils import menu, news, month_bestseller, related_news
from shop.forms import CommentForm, OrderForm
from shop.models import Shop, Comments, Customer, Notification, CartProduct, Cart, Provider, Product, \
    Order

from utils.recalc_cart import recalc_cart

from django.db.models import Q, Count
from taggit.models import Tag


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
# ---orders---------------------------------------------------------------------------------------
def index(request):
    shop = Shop.objects.all()
    shop_count = shop.count()
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()

    customers = Customer.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=customers, in_order=False).first()

    notifications = Notification.objects.all(customer_count)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('shop-orders')
    else:
        form = OrderForm()
    context = {
        'menu': menu,
        'cart': cart,
        'notifications': notifications,
        'form': form,
        'order': order,
        'shop': shop,
        'shop_count': shop_count,
        'order_count': order_count,
        'customer_count': customer_count,
    }
    return render(request, 'shop/orders.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin', 'provider'])
# ---products---------------------------------------------------------------------------------------
def products(request):
    provider = Provider.objects.all()
    shop = Shop.objects.all()
    shop_count = shop.count()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    order = Order.objects.all()
    order_count = order.count()
    shop_stock= Shop.objects.filter(name='')
    customers = Customer.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=customers, in_order=False).first()
    users = User.objects.all()
   
    recipient = Customer.objects.filter(user=request.user).first()
    notifications = Notification.objects.filter(recipient=recipient, read=False)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            shop_name = form.cleaned_data.get('name')
            messages.success(request, f'{shop_name} has been added')
            return redirect('shop-products')
    else:
        form = ProductForm()
    context = {
        'users': users,
        'provider': provider,
        'shop': shop,
        'form': form,
        'menu': menu,
        'cart': cart,
        'notifications': notifications,
        'customer_count': customer_count,
        'shop_count': shop_count,
        'order_count': order_count,
    }
    return render(request, 'shop/products.html', context)


@login_required(login_url='user-login')
# ---products_detail--------------------------------------------------------------------------------
def product_detail(request, pk):
    context = {

    }
    return render(request, 'shop/products_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
# ---customers---------------------------------------------------------------------------------------------
def customers(request):
    provider = Provider.objects.all()
    customer = User.objects.filter(groups=2)
    customer = User.objects.all()
    customer_count = customer.count()
    users = User.objects.all()
    products = CartProduct.objects.all()
    shop = Shop.objects.all()
    shop_count = shop.count()
    order = Order.objects.all()
    order_count = order.count()
    customers = Customer.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=customers, in_order=False).first()
    
    recipient = Customer.objects.filter(user=request.user).first()
    notifications = Notification.objects.filter(recipient=recipient, read=False)
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop-orders')
    else:
        form = NotificationForm()

    context = {
        'form': form,
        'provider': provider,
        'users': users,
        'products': products,
        'order': order,
        'menu': menu,
        'cart': cart,
        'notifications': notifications,
        'shop': shop,
        'customer': customer,
        'customer_count': customer_count,
        'shop_count': shop_count,
        'order_count': order_count,
    }
    return render(request, 'shop/customers.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin'])
# ---customers_detail-----------------------------------------------------------------------------------
def customer_detail(request, pk):
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    shop = Shop.objects.all()
    shop_count = shop.count()
    order = Order.objects.all()
    order_count = order.count()
    customers = User.objects.get(id=pk)
    customeres = Customer.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=customeres, in_order=False).first()
    notifications = Notification.objects.all(customer_count)

    context = {
        'menu': menu,
        'cart': cart,
        'customers': customers,
        'notifications': notifications,
        'customeres': customeres,
        'customer_count': customer_count,
        'shop_count': shop_count,
        'order_count': order_count,

    }
    return render(request, 'shop/customers_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin', 'provider'])
# ----products_edit--------------------------------------------------------------------------------------
def product_edit(request, pk):
    customers = Customer.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=customers, in_order=False).first()
    customer = User.objects.filter(groups=2)
    customer_count = customer.count()
    notifications = Notification.objects.all(customer_count)
    item = Provider.objects.get(id=pk)
    shop = Shop.objects.all()
    shop_count = shop.count()
    order = Order.objects.all()
    order_count = order.count()

    if request.method == 'POST':
        form = ProductEditForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('shop-products')
    else:
        form = ProductEditForm(instance=item)
    context = {
        'shop_count': shop_count,
        'order_count': order_count,
        'customer_count': customer_count,
        'customer': customer,
        'form': form,
        'menu': menu,
        'cart': cart,
        'notifications': notifications,
    }
    return render(request, 'shop/products_edit.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['admin', 'provider'])
# ---products_delete--------------------------------------------------------------------------------------
def product_delete(request, pk):
    customer = User.objects.filter(groups=2)
    customers = Customer.objects.filter(user=request.user).first()
    cart = Cart.objects.filter(owner=customers, in_order=False).first()
    customer_count = customer.count()
    notifications = Notification.objects.all(customer_count)
    shop = Shop.objects.all()
    shop_count = shop.count()
    order = Order.objects.all()
    order_count = order.count()

    item = Provider.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductEditForm(request.POST, instance=item)
        item.delete()
        return redirect('shop-products')
    else:
        form = ProductEditForm(instance=item)
    context = {
        'shop_count': shop_count,
        'order_count': order_count,
        'form': form,
        'customer': customer,
        'item': item,
        'menu': menu,
        'cart': cart,
        'notifications': notifications,
        'customer_count': customer_count,
    }
    return render(request, 'shop/products_delete.html', context)


class OrderView(CartMixin, NotificationsMixin, views.View):
    # ----Account--------------------------------------------------------------------------------------------------

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.all()
        order_count = order.count()
        customer_count = Customer.objects.get(user=request.user)
        shop = Shop.objects.all()
        shop_count = shop.count()
        context = {
            'customer': customer,
            'cart': self.cart,
            'menu': menu,
            'shop': shop,
            'order': order,
            'customer_count': customer_count,
            'shop_count': shop_count,
            'order_count': order_count,
            'notifications': self.notifications(request.user)
        }
        return render(request, 'shop/order.html', context)


class ShopDetailView(CartMixin, NotificationsMixin, TagMixin, views.generic.DetailView):
    # ----Shop---------------------------------------------------------------------------------------
    
    paginate_by = 6
    model = Shop
    template_name = 'shop/shop.html'
    context_object_name = 'shop'

    def get(self, request, *args, **kwargs):
        month_bestseller, month_bestseller_qty = Shop.objects.get_month_bestseller()
        contact_list = Shop.objects.all()
        paginator = Paginator(contact_list, 6)
        page_number = request.GET.get('page')
        shop = paginator.get_page(page_number)
        page_obj = paginator.get_page(page_number)
        news = Shop.objects.order_by('-name')[:3]

        context = {
            "cart": self.cart,
            'shop_selected': 0,
            'shop': shop,
            'menu': menu,
            'tag': tag,
            'news': news,
            'page_obj': page_obj,
            'notifications': self.notifications(request.user)
        }
        if month_bestseller:
            context.update({"month_bestseller": month_bestseller, "month_bestseller_qty": month_bestseller_qty})

        return render(request, 'shop/shop.html', context)


class SearchResultsView(ListView):
    # Form Search-----------------------------------------------------------------------------------
    
    model = Shop
    template_name = "shop/shop.html"
    context_object_name = 'shop'
    paginate_by = 6

    @staticmethod
    def notifications(user):
        if user.is_authenticated:
            return Notification.objects.all(user.customer)
        return Notification.objects.none()

    def get_queryset(self):

        if self.request.GET.get('val'):
            value = self.request.GET.get('val')
            queryset = Shop.objects.filter(Q(name__contains=value) | Q(content__contains=value))
        else:
            queryset = Shop.objects.all()
        return queryset

    def listing(request):
        contact_list = Shop.objects.all()
        paginator = Paginator(contact_list, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'shop/shop.html', {'page_obj': page_obj})


    def dispatch(self, request, *args, **kwargs):
        cart = None
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        val = self.request.GET.get('val')
        news = Shop.objects.order_by('-name')[:3]

        context['search-shop'] = val
        context['menu'] = menu
        context['news'] = news
        context['notifications'] = self.notifications(self.request.user)
        context['cart'] = self.cart
        context['month_bestseller'] = month_bestseller
        return context


class CustomSuccessMessageMixin:
    # ----Custom success messege-----------------------------------------------------------------------
    
    def __init__(self):
        self.request = None

    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


# ---------------------------------------------------------------------------------------------------
def post_list(request, tag_slug=None):
    object_list = Shop.all()
    template_name = "shop/shop.html"
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'shop/shop.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})
                                                   
                                                   
# --------------------------------------------------------------------------------------------
def product_detail(request,shop, id):
        # Список похожих постов
    post_tags_ids = shop.tags.values_list('id', flat=True)
    similar_shop = Shop.published.filter(tags__in=post_tags_ids) \
        .exclude(id=shop.id)
    similar_shop = similar_shop.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    return render(request, 'shop/shopost.html', {'data': shop, 'similar_shop': similar_shop})



class TagIndexView(TagMixin, ListView):
    # ----------------------------------------------------------------------------------------------------

    model = Shop
    paginate_by = '6'
    context_object_name = 'shop'

    def get_queryset(self):
        return Shop.objects.filter(tags__slug=self.kwargs.get('tag_slug'))


class ShopPost(CustomSuccessMessageMixin, CartMixin, NotificationsMixin, FormMixin, views.generic.DetailView):
    # ----Shop post--------------------------------------------------------------------------------------------
    model = Shop
    template_name = 'shop/shopost.html'
    slug_url_kwarg = 'shopost_slug'
    context_object_name = 'shopost'
    form_class = CommentForm
    success_msg = 'Comment successfully created, please wait for moderation'


    def get_success_url(self, **kwargs):
        return reverse_lazy('shopost', kwargs={'shopost_slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['name'] = context['shopost']
        context['menu'] = menu
        context['similar_posts'] = self.object.tags.similar_objects()[:4]
        context['shop_selected'] = 0,
        return context

    def tagged(request, slug):
        tag = get_object_or_404(Tag, slug=slug)
        # Filter posts by tag name
        posts = Shop.objects.filter(tags=tag)
        context = {
            'tag': tag,
            'posts': posts,
        }
        return render(request, 'shop/shopost.html', context)


class ShopProduct(ListView):
    # ----Shop Product-------------------------------------------------------------------------------
    
    paginate_by = 9
    model = Shop
    template_name = 'shop/shop.html'
    context_object_name = 'shop'

    @staticmethod
    def notifications(user):
        if user.is_authenticated:
            return Notification.objects.all(user.customer)
        return Notification.objects.none()

    def dispatch(self, request, *args, **kwargs):
        cart = None
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = str(context['shop'][0].shop)
        context['notifications'] = self.notifications(self.request.user)
        context['cart'] = self.cart
        context['menu'] = menu
        context['news'] = news
        context['month_bestseller'] = month_bestseller
        context['shop_selected'] = context['shop'][0].shop_id
        return context

    def get_queryset(self):
        return Shop.objects.filter(shop__slug=self.kwargs['shop_slug'], is_published=True)


def update_comment_status(request, pk, type):
    # ----Update comments-------------------------------------------------------------------------------
    
    item = Comments.objects.get(pk=pk)

    if type == 'public':
        import operator
        item.status = operator.not_(item.status)
        item.save()
        template = 'shop/comment_shop.html'
        context = {'item': item, 'status_comment': 'Comment published'}
        return render(request, template, context)

    elif type == 'delete':
        item.delete()
        return HttpResponse('''
            <div class="alert alert-success">
            Comment has been deleted
            </div>
            ''')

    return HttpResponse('1')
    
    
class AccessView(CartMixin, NotificationsMixin, FormMixin, views.generic.DetailView):
    # ----Access-----------------------------------------------------------------------------------------

    def get(self, request, *args, **kwargs):
        order = Order.objects.all()
        order_count = order.count()
        shop = Shop.objects.all()
        shop_count = shop.count()
        customer_count = Customer.objects.get(user=request.user)
        context = {
            'order_count': order_count,
            'order': order,
            'customer_count': customer_count,
            'shop_count': shop_count,
            "cart": self.cart,
            'shop_selected': 0,
            'menu': menu,
            'notifications': self.notifications(request.user)
        }
        return render(request, 'access.html', context)


class LoginView(views.View):
    # ----Login-----------------------------------------------------------------------------------------
    
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
            'menu': menu,
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'login.html', context)
        
        
class RegistrationUserView(views.View):
    # ----Registration User------------------------------------------------------------------------------------------

    def get(self, request, *args, **kwargs):
        form = RegistrationUserForm(request.POST or None)
        context = {
            'menu': menu,
            'form': form,
        }
        return render(request, 'registruser.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationUserForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registruser.html', context)


class RegistrationView(views.View):
    # ----Registration-----------------------------------------------------------------------------------------
    
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
            'menu': menu,
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.nif = form.cleaned_data['nif']
            new_user.first_name = form.cleaned_data['firm']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/order/')
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)


class AccountView(CartMixin, NotificationsMixin, views.View):
    # ----Account--------------------------------------------------------------------------------------------------
    
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        context = {
            'customer': customer,
            'cart': self.cart,
            'menu': menu,
            'notifications': self.notifications(request.user)
        }
        return render(request, 'shop/account.html', context)


class CartView(CartMixin, NotificationsMixin, views.View):
    # ----Cart--------------------------------------------------------------------------------------------
    
    def get(self, request, *args, **kwargs):
        return render(request, 'shop/cart.html',
                      {"cart": self.cart, 'menu': menu, 'notifications': self.notifications(request.user)})


class AddToCartView(CartMixin, views.View):
    # ----Add To Cart---------------------------------------------------------------------------------------
    
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Product added successfully")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class DeleteFromCartView(CartMixin, views.View):
    # ----Delete From Cart---------------------------------------------------------------------------------------
    
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Product successfully deleted")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ChangeQTYView(CartMixin, views.View):
    # ----Change QTY------------------------------------------------------------------------------------------
    
    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Quantity changed successfully")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class AddToWishlist(views.View):
    # ----Add To Wishlist---------------------------------------------------------------------------------------
    
    @staticmethod
    def get(request, *args, **kwargs):
        shop = Shop.objects.get(id=kwargs['shop_id'])
        customer = Customer.objects.get(user=request.user)
        customer.wishlist.add(shop)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ClearNotificationsView(views.View):
    # ----Clear Notifications---------------------------------------------------------------------------------------
    
    @staticmethod
    def get(request, *args, **kwargs):
        Notification.objects.make_all_read(request.user.customer)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class RemoveFromWishListView(views.View):
    # ----Remove From Wish Lis---------------------------------------------------------------------------------------
    
    @staticmethod
    def get(request, *args, **kwargs):
        shop = Shop.objects.get(id=kwargs['shop_id'])
        customer = Customer.objects.get(user=request.user)
        customer.wishlist.remove(shop)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class CheckoutView(CartMixin, NotificationsMixin, views.View):
    # ----Checkout---------------------------------------------------------------------------------------
    
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form,
            'menu': menu,
            'notifications': self.notifications(request.user)
        }
        return render(request, 'shop/checkout.html', context)


class MakeOrderView(CartMixin, views.View):
    # ----Make order---------------------------------------------------------------------------------------
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            out_of_stock = []
            more_than_on_stock = []
            out_of_stock_message = ""
            more_than_on_stock_message = ""
            for item in self.cart.products.all():
                if not item.content_object.stock:
                    out_of_stock.append(' - '.join([
                        item.content_object.shop.name, item.content_object.name
                    ]))
                if item.content_object.stock and item.content_object.stock < item.qty:
                    more_than_on_stock.append(
                        {'product': ' - '.join([item.content_object.shop.name, item.content_object.name]),
                         'stock': item.content_object.stock, 'qty': item.qty}
                    )
            if out_of_stock:
                out_of_stock_products = ', '.join(out_of_stock)
                out_of_stock_message = f'The product is no longer in stock: {out_of_stock_products}. \n'

            if more_than_on_stock:
                for item in more_than_on_stock:
                    more_than_on_stock_message += f'Product: {item["product"]}. ' \
                                                  f'Stock: {item["stock"]}. ' \
                                                  f'Ordered: {item["qty"]}\n'
            error_message_for_customer = ""
            if out_of_stock:
                error_message_for_customer = out_of_stock_message + '\n'
            if more_than_on_stock_message:
                error_message_for_customer += more_than_on_stock_message + '\n'

            if error_message_for_customer:
                messages.add_message(request, messages.INFO, error_message_for_customer)
                return HttpResponseRedirect('/checkout/')

            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()

            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)

            for item in self.cart.products.all():
                item.content_object.stock -= item.qty
                item.content_object.save()

            messages.add_message(request, messages.INFO, 'Thanks for your order! Manager will contact you')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')