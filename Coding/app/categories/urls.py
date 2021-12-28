from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from .views import *
from . import views
urlpatterns = [

    path('categories-list-no-page', views.get_list_no_paginate, name='categories-list-no-page'),
    path('category/<int:pk>', views.get_details),
    path('category-and-subcate-detail', views.get_category_and_detail_subcategory),
    path('category-activate/<int:pk>', views.activate),
    url('categories', CategoryView.as_view()),
]
