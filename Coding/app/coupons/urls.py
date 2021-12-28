from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('coupon-list-no-page', views.get_list_no_paginate, name='coupon-list-no-page'),
    path('coupon/<int:pk>', views.get_details, name='coupon-get-details'),
    path('coupon-activate/<int:pk>', views.activate),
    url('coupons', CouponView.as_view()),
]
