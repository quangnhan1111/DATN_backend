from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('brand-list-no-page', views.get_list_no_paginate, name='brand-list-no-page'),
    path('brand/<int:pk>', views.get_details, name='brand-get-details'),
    path('brand-activation/<int:pk>', views.activate, name='brand-activation'),
    url('brands', BrandView.as_view()),
]
