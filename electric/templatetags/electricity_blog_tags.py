from django import template
from flask.json import tag
from taggit.models import Tag

from blog.models import Category, Blog

register = template.Library()


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

# ------------------------------------------------------------------------------------
@register.inclusion_tag('list_cats.html')
def show_categories(sort=None, blog_selected=0):
    if not sort:
        blog = Category.objects.all()
    else:
        blog = Category.objects.order_by(sort)

    return {"blog": blog, "blog_selected": blog_selected}


# -----------------------------------------------------------------------------------
@register.simple_tag(name='tages')
def get_tages(filter=None):
    if not filter:
        return Tag.objects.all()
    else:
        return Tag.objects.filter(slug=filter)

# ------------------------------------------------------------------------------------
@register.inclusion_tag('list_cats.html')
def show_tages(sort=None, tages_selected=0):
    if not sort:
        tag = Tag.objects.all()
    else:
        tag = Tag.objects.order_by(sort)

    return {"tag": tag, "tages_selected": tages_selected}