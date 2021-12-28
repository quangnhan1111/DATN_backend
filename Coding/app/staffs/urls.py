from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('auth/staff-login', LoginProfileView.as_view(), name='login-staff'),

    path('staff/<int:pk>', views.get_details),
    path('staff-activate/<int:pk>', views.activate),
    path('admin/staff/get-all', views.get_list_admin_and_staff, name='staff-list-no-page'),
    path('admin/staffs', ProfileView.as_view()),

    path('admin/staff/change-password/<int:pk>', views.change_password),


]
