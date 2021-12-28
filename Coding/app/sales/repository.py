from django.db.models import Sum
from django.db.models import F, Value
from invoice_detail.models import InvoiceDetail
from invoices.models import Invoice
from staffs.models import Staff
from customers.models import Customer as CustomerModel
from django.db.models.functions import Extract, Concat


class SaleRepository:
    def __init__(self):
        pass

    def get_totel_user(self):
        customers = CustomerModel.objects.filter(deleted_at=False).order_by('-id')
        staffs = Staff.objects.filter(deleted_at=False, user__groups__name='staff') \
            .exclude(user__groups__name='admin').order_by('id')
        return [customers.count(), staffs.count()]

    def get_total_product_sold_out(self):
        total_product_sold_out = InvoiceDetail.objects.all().aggregate(Sum('number'))['number__sum']
        print(total_product_sold_out)
        return total_product_sold_out

    def get_sale_figure_by_day(self):
        sale_by_day = Invoice.objects.order_by('-id').exclude(staff_id=None).annotate(total_sale=Sum('totalPrice'),
                                                                                      Day=Extract('updated_at', 'day'),
                                                                                      Month=Extract('updated_at',
                                                                                                    'month'),
                                                                                      Year=Extract('updated_at',
                                                                                                   'year'), ) \
            .values('total_sale', 'Day', 'Month', 'Year')
        print(sale_by_day)
        return sale_by_day

    def get_sale_figure_by_month(self):
        sale_by_month = Invoice.objects.exclude(staff_id=None).annotate(total_sale=Sum('totalPrice'),
                                                                        Month=Extract('updated_at', 'month'),
                                                                        Year=Extract('updated_at', 'year'), ) \
            .values('total_sale', 'Month', 'Year')
        print(sale_by_month.query)
        return sale_by_month

    def get_sale_figure_by_staff(self):
        print("S")
        data = Staff.objects.filter(deleted_at=False, status=True).exclude(user__groups__name='admin').annotate(IdStaff=F('id'),
                                                                                                   FullNameStaff=Concat(
                                                                                                       'user__first_name',
                                                                                                       Value(' '),
                                                                                                       'user__last_name'),
                                                                                                   EmailStaff=F(
                                                                                                       'user__email'),
                                                                                                   total_sale=Sum(
                                                                                                       'invoice__totalPrice'),

                                                                                                   Month=Extract(
                                                                                                       'invoice__updated_at',
                                                                                                       'month'),
                                                                                                   Year=Extract(
                                                                                                       'invoice__updated_at',
                                                                                                       'year'), ) \
            .values('Month', 'Year', 'IdStaff', 'FullNameStaff', 'total_sale', 'EmailStaff', 'address', 'phone_number').order_by(
            '-total_sale')
        print(data)
        return data
