from django.conf.urls import url
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('role/get-users-by-role/<int:pk>', views.get_users_by_role, name='get-users-by-role'),
    path('role/get-role-by-user/<int:pk>', views.get_role_by_user, name='get-role-by-user'),
    path('role/<int:pk>', views.get_details),
    url('roles', RoleView.as_view()),
]
