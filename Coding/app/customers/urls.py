
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('verify/<auth_token>', Verify.as_view(), name="verify"),
    # path('reset-password', Reset.as_view(), name="verify"),
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view()),

    path('customer/<int:pk>', views.get_details),
    path('admin/customer/get-all', views.get_list_no_paginate),
    path('customer-activate/<int:pk>', views.activate),
    path('admin/customers/change-password/<int:pk>', views.change_password),
    path('admin/customers', CustomerView.as_view()),

]
