from django.contrib import admin

from electric.models import Category
from shop.models import CartProduct, Order, Customer, Notification, Product, Shop, ImageGallery, Cart, Comments, Provider

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import *


class ImageGalleryInline(GenericTabularInline):

    model = ImageGallery
    readonly_fields = ('image_url',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo', 'price', 'stock', 'available', 'created', 'updated')

    list_display_links = ('id', 'name')
    search_fields = ('name', 'content')
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'shop', 'main_content', 'content', 'photo', 'price', 'stock', 'tags', 'is_published', 'get_html_photo', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    inlines = [ImageGalleryInline]
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Miniature"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class ImgProjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'first_name', 'last_name', 'phone', 'cart')
    list_display_links = ('id', 'first_name')
    search_fields = ('id','customer', 'first_name')
    list_filter = ('id','customer', 'first_name')
    
    
@admin.register(Provider)
class Provider(admin.ModelAdmin):
    list_display = ('id', 'firm', 'nif', 'phone', 'name', 'price', 'stock', 'available', 'created', 'updated')

    list_display_links = ('id', 'name')
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'stock', 'available')
    fields = ('firm', 'nif', 'phone', 'address', 'name', 'shop', 'price', 'discount', 'iva', 'total', 'stock', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update')
    

admin.site.register(ImageGallery)
admin.site.register(Product, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Customer)
admin.site.register(Notification)
admin.site.register(Comments)
