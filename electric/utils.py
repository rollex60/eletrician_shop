from shop.models import Shop
from .models import *

menu = [{'name': "About", 'url_name': "about"},
        {'name': "Services", 'url_name': "services"},
        {'name': "Price", 'url_name': "prices"},
        {'name': "Gallery", 'url_name': "gallery"},
        {'name': "Blog", 'url_name': "blog"},
        {'name': "Shop", 'url_name': "shop"},
        {'name': "Contact", 'url_name': "contact"},
]

news = Shop.objects.order_by('-name')[:3]
month_bestseller, month_bestseller_qty = Shop.objects.get_month_bestseller()
related_news = Shop.objects.order_by('-name')[:4]