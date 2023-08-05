from django import template
from electric.models import *
from shop.models import Product

register = template.Library()


@register.simple_tag(name='getprod')
# -------------------------------------------------------------------------------------
def get_products(filter=None):
    if not filter:
        return Product.objects.all()
    else:
        return Product.objects.filter(pk=filter)


@register.inclusion_tag('list_categories.html')
# -------------------------------------------------------------------------------------
def show_products(sort=None, shop_selected=0):
    if not sort:
        shop = Product.objects.all()
    else:
        shop = Product.objects.order_by(sort)

    return {"shop": shop, "shop_selected": shop_selected}



