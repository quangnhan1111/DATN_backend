from django.urls import path

from . import views

urlpatterns = [
    path('saleFigure/get-total-user', views.get_totel_user, name='getTotalUser'),
    path('saleFigure/get-total-product-sold-out', views.get_total_product_sold_out, name='getTotalProductSoldOut'),
    path('saleFigure/get-sale-figure-by-day', views.get_sale_figure_by_day, name='getSaleFigureByDay'),
    path('saleFigure/get-sale-figure-by-month', views.get_sale_figure_by_month, name='getSaleFigureByMonth'),
    path('saleFigure/get-sale-figure-by-staff', views.get_sale_figure_by_staff, name='getSaleFigureByEmployee'),
]
