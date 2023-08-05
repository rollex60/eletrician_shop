import operator
from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.utils import connection, timezone
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager

from utils.uploading import upload_function

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import connection


class ShopManager(models.Manager):
# ----Shop manager---------------------------------------------------------------------------------------

    def get_queryset(self):
        return super().get_queryset()

    def get_month_bestseller(self):
        today = datetime.today()
        year, month = today.year, today.month
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, monthrange(year, month)[1])
        query = f"""
                    SELECT shop_product.id as product_id, SUM(distinct shop_cart_product.qty) as total_qty
                    FROM shop_order as shop_order
                    JOIN shop_cart as shop_cart on shop_order.cart_id = shop_cart.id
                    JOIN shop_cartproduct as shop_cart_product on shop_cart.id = shop_cart_product.cart_id
                    JOIN shop_shop as shop_product on shop_cart_product.object_id=shop_product.id
                    WHERE shop_order.order_date >= '{first_day}' and shop_order.order_date <= '{last_day}'
                    GROUP BY product_id
                    ORDER BY total_qty DESC
                    LIMIT 1
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
        if row:
            product_id, qty = row
            shop = Shop.objects.get(pk=product_id)
            return shop, qty
        return None, None


class Shop(models.Model):
    # ----Shop---------------------------------------------------------------------------------------------
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Article author', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    main_content = RichTextUploadingField(verbose_name="Main content", blank=True, null=True)
    content = RichTextUploadingField(verbose_name="Contente", blank=True, null=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, verbose_name="Photo")
    available = models.BooleanField(default=True, verbose_name="Accessible")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")
    is_published = models.BooleanField(default=True, verbose_name="Is published")
    shop = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='shop', verbose_name="Product")
    stock = models.IntegerField(default=1, verbose_name='Availability in stock')
    out_of_stock = models.BooleanField(default=False, verbose_name='Not available')
    image_gallery = GenericRelation('imagegallery')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    offer_of_the_week = models.BooleanField(default=False, verbose_name='Deal of the week?')
    image = models.ImageField(upload_to=upload_function)
    objects = ShopManager()
    tags = TaggableManager()

    def __str__(self):
        return f"{self.id} | {self.name}"

    @property
    def ct_model(self):
        return self._meta.model_name

    def get_absolute_url(self):
        return reverse('shopost', kwargs={'shopost_slug': self.slug})

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shop'
        ordering = ['-id']
        
        
class Provider(models.Model):
    # ----Provider---------------------------------------------------------------------------------------------
    
    firm = models.ForeignKey (User, on_delete=models.CASCADE, verbose_name='Article author', blank=True, null=True)
    nif = models.CharField(max_length=9, verbose_name='NIF')
    phone = models.CharField(max_length=20, verbose_name='Telephone')
    address = models.CharField(max_length=1024, verbose_name='Address', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Title")
    shop = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='shop_provider', verbose_name="Product")
    available = models.BooleanField(default=True, verbose_name="Accessible")
    stock = models.IntegerField(default=1, verbose_name='Availability in stock')
    out_of_stock = models.BooleanField(default=False, verbose_name='Not available')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Discount')
    iva = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='IVA')
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Total')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Update time")

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        self.total = (self.iva * (self.stock * self.price - self.discount * self.stock * self.price)) + \
                    ((self.stock * self.price) - (self.discount * self.stock * self.price))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('provider', kwargs={'provider_slug': self.slug})

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
        ordering = ['-id']


class Product(models.Model):
    # ----Products----------------------------------------------------------------------------------------
    
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'
        ordering = ['id']

    # Link to category
    def get_absolute_url(self):
        return reverse('shop', kwargs={'shop_slug': self.slug})


class CartProduct(models.Model):
    # ----Cart product-----------------------------------------------------------------------------------------
    
    MODEL_CARTPRODUCT_DISPLAY_NAME_MAP = {
        "Shop": {"is_constructable": True, "fields": ["name", "product.name"], "separator": ' - '}
    }

    user = models.ForeignKey('Customer', verbose_name='Buyer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price')

    def __str__(self):
        return f"Product: {self.content_object.name} (for the cart)"

    @property
    def display_name(self):
        model_fields = self.MODEL_CARTPRODUCT_DISPLAY_NAME_MAP.get(self.content_object.__class__._meta.model_name.capitalize())
        if model_fields and model_fields['is_constructable']:
            display_name = model_fields['separator'].join(
                [operator.attrgetter(field)(self.content_object) for field in model_fields['fields']]
            )
            return display_name
        if model_fields and not model_fields['is_constructable']:
            display_name = operator.attrgetter(model_fields['field'])(self.content_object)
            return display_name

        return self.content_object

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cart product'
        verbose_name_plural = 'Cart products'


class Cart(models.Model):
    # ----Cart--------------------------------------------------------------------------------------------
    
    owner = models.ForeignKey('Customer', verbose_name='Buyer', on_delete=models.CASCADE)
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name='related_cart', verbose_name='Shopping cart products'
    )
    total_products = models.IntegerField(default=0, verbose_name='Total number of goods')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price', null=True, blank=True)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def products_in_cart(self):
        return [c.content_object for c in self.products.all()]

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class Order(models.Model):
    # ----User order----------------------------------------------------------------------------------------
    
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS, 'Order in processing'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Order received by customer')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Pickup'),
        (BUYING_TYPE_DELIVERY, 'Delivery')
    )

    customer = models.ForeignKey('Customer', verbose_name='Buyer', related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Name')
    last_name = models.CharField(max_length=255, verbose_name='Surname')
    phone = models.CharField(max_length=20, verbose_name='Telephone')
    cart = models.ForeignKey(Cart, verbose_name='Basket', null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=1024, verbose_name='Address', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Order status', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(max_length=100, verbose_name='Order type', choices=BUYING_TYPE_CHOICES)
    comment = models.TextField(verbose_name='Comment to the order', null=True, blank=True)
    created_at = models.DateField(verbose_name='Order creation date', auto_now=True)
    order_date = models.DateField(verbose_name='Date of receipt of the order', default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Customer(models.Model):
    # ----Buyer-------------------------------------------------------------------------------------------------
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='Active?')
    customer_orders = models.ManyToManyField(
        Order, blank=True, verbose_name='Buyer orders',related_name='related_customer'
    )
    wishlist = models.ManyToManyField(Shop, blank=True, verbose_name='List of expected')
    phone = models.CharField(max_length=20, verbose_name='Phone number')
    address = models.TextField(null=True, blank=True, verbose_name='Address')

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyers'


class Comments(models.Model):
    # ----Comments----------------------------------------------------------------------------------------------
    
    article = models.ForeignKey(Shop, on_delete=models.CASCADE,
                                verbose_name='shopost', blank=True, null=True, related_name='comments_shop')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User comments', blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Article comments')
    status = models.BooleanField(verbose_name='Article visibility', default=False)

    class Meta:
        verbose_name = 'Comments'
        verbose_name_plural = 'Comments'
        ordering = ['-id']


class NotificationManager(models.Manager):
    # ----Notification manager---------------------------------------------------------------------------------------
    
    def get_queryset(self):
        return super().get_queryset()

    def all(self, recipient):
        return self.get_queryset().filter(
            recipient=recipient,
            read=False
        )

    def make_all_read(self, recipient):
        qs = self.get_queryset().filter(recipient=recipient, read=False)
        qs.update(read=True)


class Notification(models.Model):
    # ----Notifications---------------------------------------------------------------------------------------
    
    recipient = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Recipient')
    text = models.TextField()
    read = models.BooleanField(default=False)
    objects = NotificationManager()

    def __str__(self):
        return f"Notice for {self.recipient.user.username} | id={self.id}"

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notification'


class ImageGallery(models.Model):
    # ----Image Gallery---------------------------------------------------------------------------------------
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_function)
    use_in_slider = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.content_object}"

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="200px"')

    class Meta:
        verbose_name = 'Image Gallery'
        verbose_name_plural = verbose_name


def check_previous_qty(instance, **kwargs):
    try:
        shop = Shop.objects.get(id=instance.id)
    except Shop.DoesNotExist:
        return None
    instance.out_of_stock = True if not shop.stock else False


def send_notification(instance, **kwargs):
    if instance.stock and instance.out_of_stock:
        customers = Customer.objects.filter(
            wishlist__in=[instance]
        )
        if customers.count():
            for c in customers:
                Notification.objects.create(
                    recipient=c,
                    text=mark_safe(f'Position <a href="{instance.get_absolute_url()}">{instance.name}</a>, '
                                   f'what you expect is in stock.')
                )
                c.wishlist.remove(instance)


post_save.connect(send_notification, sender=Shop)
pre_save.connect(check_previous_qty, sender=Shop)



