from django.conf.urls import url
from django.urls import path
from .views import *
from . import views
urlpatterns = [

    path('subcates-list-no-page', views.get_list_no_paginate, name='subcategories-list-no-page'),
    path('subcate/<int:pk>', views.get_details),
    path('subcate-activate/<int:pk>', views.activate),
    path('category/<int:pk>/subcate', views.get_sub_base_on_category),
    url('subcates', SubCategoryView.as_view()),
]
