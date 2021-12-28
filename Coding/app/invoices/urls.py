from django.conf.urls import url
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # client
    path('invoice/getInvoicesForOneCustomerStatus/<int:pk>', views.getInvoicesForOneCustomerStatus,
         name='getInvoicesForOneCustomerStatus'),
    path('invoice/showOneInvoicesAndShowCustomer/<int:pk>', views.showOneInvoicesAndShowCustomer,
         name='showInvoicesByIdEmployee'),
    path('invoice/getInvoicesForEmployeeStatus', views.getInvoicesForEmployeeStatus, name='getInvoicesForEmployeeStatus'),


    path('invoice/getInvoicesByCustomer', views.getInvoicesByCustomer, name='getInvoicesByCustomer'),
    path('invoice/getInvoicesByEmployee', views.getInvoicesByEmployee, name='getInvoicesByEmployee'),
    path('invoice/getInvoicesForOneEmployeeStatus/<int:pk>', views.getInvoicesForOneEmployeeStatus, name='getInvoicesForOneEmployeeStatus'),
    path('invoice/getInvoicesForCustomerStatus', views.getInvoicesForCustomerStatus, name='getInvoicesForCustomerStatus'),
    path('invoice/showOneInvoices/<int:pk>', views.showOneInvoices, name='showOneInvoices'),
    path('invoice/showOneInvoicesAndShowEmployee/<int:pk>', views.showOneInvoicesAndShowEmployee, name='getInvoicesForOneEmployeeStatus'),
    path('invoice/showInvoicesByIdEmployee/<int:pk>', views.showInvoicesByIdEmployee, name='showInvoicesByIdEmployee'),
    path('invoice/showInvoicesByIdCustomer/<int:pk>', views.showInvoicesByIdCustomer, name='showInvoicesByIdEmployee'),

    # path('invoice/<int:pk>/', DetailInvoice.as_view(), name='posts-detail'),
    url('invoices', InvoiceView.as_view()),
]
