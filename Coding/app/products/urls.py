from django.conf.urls import url
from django.urls import path

from .views import *
from . import views

urlpatterns = [
    path('client/product/search/<str:key>', views.get_product_by_search, name='search-results'),
    path('client/product/wishlist/customer/<int:idCustomer>', views.get_wishlist_product, name='get_wishlist_product'),
    path('client/product/wishlist/customer/<int:idCustomer>/check/<int:idPro>', views.check_wishlist_product, name='check_wishlist_product'),
    path('client/product/new', views.get_new_product, name='new-results'),
    path('client/product/best', views.get_best_product, name='best-results'),
    path('client/brand/relateProduct/<int:pk>', views.get_related_product_by_brand, name='relate-by-brand-results'),
    path('client/subcategory/relateProduct/<int:pk>', views.get_related_product_by_subcate, name='relate-by-subcate'
                                                                                                 '-results'),
    path('client/category/relateProduct/<int:pk>', views.get_related_product_by_cate, name='get_related_product_by_cate'),

    path('client/product/search-base-price/<str:price_min>/<str:price_max>', views.search_base_price, name='search_base_price'),
    path('client/product/search-base-review/<int:rating>', views.search_base_review, name='search_base_review'),
    path('client/product/search-base-size/<str:name_size>', views.search_base_size, name='search_base_size'),

    path('client/product/sorted-Low-to-High', views.sorted_low_to_high, name='sorted_low_to_high'),
    path('client/product/sorted-Hight-to-Low', views.sorted_high_to_low, name='sorted_high_to_low'),

    path('product/<int:pk>', views.get_details),
    path('product-activate/<int:pk>', views.activate),
    path('product-list', views.get),
    path('product-list-no-page', views.get_list_no_page),

    path('product-rs', views.RS),

    # path('product-rc', views.get_rc),
    url('products', ProductView.as_view(), name='products'),
]
