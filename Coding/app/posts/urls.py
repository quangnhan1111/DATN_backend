from django.conf.urls import url
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('post/<int:pk>', views.get_details),
    path('post-list', views.get_list, name='post-list'),
    path('post-activate/<int:pk>', views.activate),
    path('post-list-no-page', views.get_list_no_page, name='get_list_no_page'),
    url('posts', PostView.as_view()),
]
