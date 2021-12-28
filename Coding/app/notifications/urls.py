from django.conf.urls import url
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('notifications', views.notifications, name='notifications'),
    path('mark/<int:pk>', views.mark, name='notifications_mark'),
    path('clear-all-notifications', views.clear_all_notification, name='clear_all_notification'),

    path('message', views.message_notifications, name='message'),
    path('mark_message/<int:pk>', views.mark_message, name='message_mark'),
    path('clear-all-messages', views.clear_all_message, name='clear_all_message'),

    path('invoice_notify', views.invoice_notifications, name='invoice'),


]
