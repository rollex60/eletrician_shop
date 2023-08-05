from django.contrib.admin.templatetags.admin_list import search_form
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

from .views import *
from . import views


urlpatterns = [
    # endpoint to cart
    path('', search_form, name='search_form_url'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_qty'),
    path('shop/', ShopDetailView.as_view(), name='shop'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    path('shopost/<slug:shopost_slug>/', ShopPost.as_view(), name='shopost'),
    path('tags/<slug:tag_slug>/', TagIndexView.as_view(), name='tagged'),
    path("search-shop/", SearchResultsView.as_view(), name="search_results"),

    path('shop/<slug:shop_slug>/', ShopProduct.as_view(), name='shop'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registruser/', RegistrationUserView.as_view(), name='registruser'),
    
    path('account/', AccountView.as_view(), name='account'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('clear-notifications/', ClearNotificationsView.as_view(), name='clear-notifications'),
    path('add-to-whishlist/<int:shop_id>/', AddToWishlist.as_view(), name='add_to_wishlist'),
    path('remove-from-wishlist/<int:shop_id>/', RemoveFromWishListView.as_view(), name='remove_from_wishlist'),
    path('make-order/', MakeOrderView.as_view(), name='make-order'),
    
    path('index/', views.index, name='shop-orders'),
    path('access/', AccessView.as_view(), name='access'),
    path('products/', views.products, name='shop-products'),
    path('products/delete/<int:pk>/', views.product_delete,
         name='shop-products-delete'),
    path('products/detail/<int:pk>/', views.product_detail,
         name='shop-products-detail'),
    path('products/edit/<int:pk>/', views.product_edit,
         name='shop-products-edit'),
    path('customers/', views.customers, name='shop-customers'),
    path('customers/detial/<int:pk>/', views.customer_detail,
         name='shop-customer-detail'),
    path('order/', OrderView.as_view(), name='shop-order'),

    #ajax
    path('update_comment_status/<int:pk>/<slug:type>', views.update_comment_status, name='update_comment_status')
]