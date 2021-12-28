from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from .views import *
from . import views
urlpatterns = [

    path('colors/get-by-product/<int:product_id>', views.get_color_by_product),
    path('sizes/get-by-product/<int:product_id>', views.get_size_by_product),
    path('color-list-no-page', views.get_list_no_paginate, name='color-list-no-page'),
    path('color/<int:pk>', views.get_details),
    path('color-activate/<int:pk>', views.active),
    url('colors', ColorView.as_view()),
]
