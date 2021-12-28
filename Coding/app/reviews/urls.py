from django.conf.urls import url
from django.urls import path

from .views import *
from . import views

urlpatterns = [
    path('reviews/product/<int:pk>', views.get_all_review_by_product, name='get-review'),
    path('reviews/good/', views.get_good_review, name='good-review'),

    path('review/<int:pk>', views.get_details),
    url('reviews', ReviewView.as_view()),
]


