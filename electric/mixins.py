from django import views
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render
from taggit.models import Tag

from blog.models import Blog
from electric.utils import menu, news, month_bestseller
from shop.models import Notification, Customer, Cart, Shop


class NotificationsMixin(views.generic.detail.SingleObjectMixin):
    # -Notifications--------------------------------------------------------------------------------------

    @staticmethod
    def notifications(user):
        if user.is_authenticated:
            return Notification.objects.all(user.customer)
        return Notification.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications'] = self.notifications(self.request.user)
        return context


class CartMixin(views.generic.detail.SingleObjectMixin, views.View):
    # --Cart--------------------------------------------------------------------------------------

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
        context['cart'] = self.cart
        return context


class TagMixin(object):
    # -Tag---------------------------------------------------------------------------------------
    
    model = Shop
    template_name = "shop/shop.html"
    context_object_name = 'tag'
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

    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['menu'] = menu
        context['news'] = news
        context['notifications'] = self.notifications(self.request.user)
        context['cart'] = self.cart
        context['month_bestseller'] = month_bestseller
        return context


class TagMixinBlog(object):
    # --Tag-------------------------------------------------------------------------------
    
    model = Blog
    template_name = "blog/blog.html"
    context_object_name = 'tag'
    paginate_by = 6

    @staticmethod
    def notifications(user):
        if user.is_authenticated:
            return Notification.objects.all(user.customer)
        return Notification.objects.none()

    def get_queryset(self):

        if self.request.GET.get('val'):
            value = self.request.GET.get('val')
            queryset = Blog.objects.filter(Q(name__contains=value) | Q(content__contains=value))
        else:
            queryset = Blog.objects.all()
        return queryset

    def listing(request):
        contact_list = Blog.objects.all()
        paginator = Paginator(contact_list, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/blog.html', {'page_obj': page_obj})

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
        context = super(TagMixinBlog, self).get_context_data(**kwargs)
        context['tages'] = Blog.tages.annotate(blog_count=Count('tages'))
        context['menu'] = menu

        context['notifications'] = self.notifications(self.request.user)
        context['cart'] = self.cart

        return context



