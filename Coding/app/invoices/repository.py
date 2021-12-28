from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import F

from invoice_detail.models import InvoiceDetail
from products.models import Attribute_Int
from .models import Invoice
from .serializer import InvoiceSerializer


class InvoiceRepository:
    def __init__(self):
        pass

    def get_invoices_by_customer(self):
        invoices = Invoice.objects.filter(deleted_at=False).order_by('id') \
            .annotate(numberSoldOut=F('invoicedetail__number'),
                      nameProduct=F('invoicedetail__product__name'),
                      nameSizeProduct=F('invoicedetail__name_size'),
                      priceProduct=F('invoicedetail__price'),
                      TotalNumberWareProduct=F('invoicedetail__product__attribute_int__value'),
                      NameColors=F('invoicedetail__name_color'),
                      NameGender=F('invoicedetail__product__gender'),
                      link=F('invoicedetail__product__image_link'),
                      FullNameCustomer=F('customer__user__last_name') + ' ' + F('customer__user__first_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'numberSoldOut', 'nameProduct',
                    'nameSizeProduct', 'priceProduct',
                    'TotalNumberWareProduct', 'NameColors', 'NameGender', 'link',
                    'FullNameCustomer', 'TotalForPay')

        print(invoices.query)
        return invoices

    def get_invoices_by_staff(self):
        invoices = Invoice.objects.filter(deleted_at=False).order_by('id') \
            .annotate(numberSoldOut=F('invoicedetail__number'),
                      nameProduct=F('invoicedetail__product__name'),
                      nameSizeProduct=F('invoicedetail__name_size'),
                      priceProduct=F('invoicedetail__price'),
                      TotalNumberWareProduct=F('invoicedetail__product__attribute_int__value'),
                      NameColors=F('invoicedetail__name_color'),
                      NameGender=F('invoicedetail__product__genders__name'),
                      link=F('invoicedetail__product__images__link'),
                      FullNameEmployee=F('staff__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'numberSoldOut', 'nameProduct',
                    'nameSizeProdcut', 'priceProdcut',
                    'TotalNumberWareProduct', 'NameColors', 'NameGender', 'link',
                    'FullNameEmployee', 'TotalForPay')

        print(invoices.query)
        return invoices

    def getInvoicesForEmployeeStatus(self):
        invoices = Invoice.objects.filter(deleted_at=False).order_by('id') \
            .annotate(IdEmployee=F('staff__user_id'),
                      FullNameCustomer=F('customer__user__last_name'),
                      FullNameEmployee=F('staff__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'full_name', 'address', 'phone_number', 'email', 'message',
                    'IdEmployee', 'TotalForPay', 'FullNameCustomer', 'FullNameEmployee').order_by('-id')

        print(invoices.query)
        return invoices

    def getInvoicesForCustomerStatus(self):
        invoices = Invoice.objects.filter(deleted_at=False).order_by('id') \
            .annotate(IdCustomer=F('customer__user_id'),
                      FullNameCustomer=F('customer__user__last_name'),
                      FullNameEmployee=F('staff__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'full_name', 'address', 'phone_number', 'email', 'message',
                    'IdCustomer', 'TotalForPay', 'FullNameCustomer', 'FullNameEmployee')

        print(invoices.query)
        return invoices

    def getInvoicesForOneEmployeeStatus(self, pk):

        invoices = Invoice.objects.filter(deleted_at=False, staff_id=pk).order_by('id').values() \
            .annotate(IdEmployee=F('staff__user_id'),
                      FullNameCustomer=F('customer__user__last_name'),
                      FullNameEmployee=F('staff__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'full_name', 'address', 'phone_number', 'email', 'message',
                    'IdEmployee', 'TotalForPay', 'FullNameCustomer', 'FullNameEmployee', )

        # invoices = Invoice.objects.filter(deleted_at=False, employee_id=pk).order_by('id').values()

        print(invoices.query)
        return invoices

    def getInvoicesForOneCustomerStatus(self, pk):
        invoices = Invoice.objects.filter(deleted_at=False, customer_id=pk).order_by('id') \
            .annotate(IdCustomer=F('customer__user_id'),
                      FullNameCustomer=F('customer__user__last_name'),
                      FullNameEmployee=F('staff__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'full_name', 'address', 'phone_number', 'email', 'message',
                    'IdCustomer', 'TotalForPay', 'FullNameCustomer', 'FullNameEmployee')

        print(invoices.query)
        return invoices

    def showOneInvoices(self, pk):
        invoices = Invoice.objects.filter(deleted_at=False, id=pk).order_by('id') \
            .annotate(FullNameCustomer=F('customer__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'full_name', 'address', 'phone_number', 'email', 'message',
                    'TotalForPay', 'FullNameCustomer')

        print(invoices.query)
        return invoices

    def showOneInvoicesAndShowEmployee(self, pk):
        invoices = Invoice.objects.filter(deleted_at=False, id=pk).order_by('id') \
            .annotate(numberSoldOut=F('invoicedetail__number'),
                      nameProduct=F('invoicedetail__product__name'),
                      nameSizeProduct=F('invoicedetail__name_size'),
                      priceProduct=F('invoicedetail__price'),
                      TotalNumberWareProduct=F('invoicedetail__product__attribute_int__value'),
                      NameColors=F('invoicedetail__name_color'),
                      NameGender=F('invoicedetail__product__genders__name'),
                      link=F('invoicedetail__product__images__link'),
                      FullNameEmployee=F('staff__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'numberSoldOut', 'nameProduct',
                    'nameSizeProdcut', 'priceProdcut',
                    'TotalNumberWareProduct', 'NameColors', 'NameGender', 'link',
                    'FullNameEmployee', 'TotalForPay')
        print(invoices.query)
        return invoices

    def showInvoicesByIdEmployee(self, pk):
        invoices = Invoice.objects.filter(deleted_at=False, staff__user_id=pk).order_by('id') \
            .annotate(numberSoldOut=F('invoicedetail__number'),
                      nameProduct=F('invoicedetail__product__name'),
                      nameSizeProduct=F('invoicedetail__name_size'),
                      priceProduct=F('invoicedetail__price'),
                      TotalNumberWareProduct=F('invoicedetail__product__attribute_int__value'),
                      NameColors=F('invoicedetail__name_color'),
                      NameGender=F('invoicedetail__product__genders__name'),
                      link=F('invoicedetail__product__images__link'),
                      FullNameEmployee=F('staff__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'numberSoldOut', 'nameProduct',
                    'nameSizeProduct', 'priceProduct',
                    'TotalNumberWareProduct', 'NameColors', 'NameGender', 'link',
                    'FullNameEmployee', 'TotalForPay')
        print(invoices.query)
        return invoices

    def showInvoicesByIdCustomer(self, pk):
        invoices = Invoice.objects.filter(deleted_at=False, customer__user_id=pk).order_by('id') \
            .annotate(numberSoldOut=F('invoicedetail__number'),
                      nameProduct=F('invoicedetail__product__name'),
                      nameSizeProduct=F('invoicedetail__name_size'),
                      priceProduct=F('invoicedetail__price'),
                      TotalNumberWareProduct=F('invoicedetail__product__attribute_int__value'),
                      NameColors=F('invoicedetail__name_color'),
                      NameGender=F('invoicedetail__product__genders__name'),
                      link=F('invoicedetail__product__images__link'),
                      FullNameCustomer=F('customer__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'numberSoldOut', 'nameProduct',
                    'nameSizeProduct', 'priceProduct',
                    'TotalNumberWareProduct', 'NameColors', 'NameGender', 'link',
                    'FullNameCustomer', 'TotalForPay')
        print(invoices.query)
        return invoices

    def showOneInvoicesAndShowCustomer(self, pk):


        data = Invoice.objects.values('invoicedetail__product__name')
        invoices = Invoice.objects.filter(deleted_at=False, id=pk).order_by('id') \
            .annotate(
                      numberSoldOut=F('invoicedetail__number'),
                      nameProduct=F('invoicedetail__product__name'),
                      nameSizeProduct=F('invoicedetail__name_size'),
                      priceProduct=F('invoicedetail__price'),
                      TotalNumberWareProduct=F('invoicedetail__product__attribute_int__value'),
                      NameColors=F('invoicedetail__name_color'),
                      NameGender=F('invoicedetail__product__gender'),
                      link=F('invoicedetail__product__image_link'),
                      FullNameCustomer=F('customer__user__last_name'),
                      TotalForPay=F('totalPrice'),
                      ) \
            .values('id', 'is_paid', 'numberSoldOut', 'nameProduct',
                    'nameSizeProduct', 'priceProduct',
                    'TotalNumberWareProduct', 'NameColors', 'NameGender', 'link',
                    'FullNameCustomer', 'TotalForPay')
        print(invoices.query)
        return invoices

    def update(self, objUpdate, request):
        # old_name = objUpdate.id
        print(request.data['employee_id'])
        objUpdate.is_paid = request.data['is_paid']
        if not request.data['is_paid']:
            objUpdate.staff_id = None
        else:
            objUpdate.staff_id = request.data['employee_id']
        objUpdate.save()
        serializer = InvoiceSerializer(objUpdate)
        try:
            # notifications
            count = Invoice.objects.filter(is_paid=False).count()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'invoice_notification', {
                    'type': 'send.invoice_notification',
                    'value': str(count)
                }
            )
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def store(self, request):
        objUpdate = Invoice()
        objUpdate.message = request.data['message']
        objUpdate.email = request.data['email']
        objUpdate.address = request.data['address']
        objUpdate.phone_number = request.data['phone_number']
        objUpdate.full_name = request.data['full_name']
        objUpdate.is_paid = request.data['is_paid']
        objUpdate.customer_id = request.data['customer_id']
        objUpdate.employee_id = request.data['employee_id']
        objUpdate.gateway = request.data['gateway']
        # objUpdate.gateway = request.data['coupon']
        objUpdate.totalPrice = 0
        objUpdate.save()
        all_id_product = list()
        total_price = 0
        err = ''
        for i in range(0, len(request.data['listProduct'])):
            product_attribute_int = Attribute_Int.objects.get(
                product_id=request.data['listProduct'][i]['product__product_link']
            )
            print(product_attribute_int)
            # product = Product.objects.get(pk=request.data['listProduct'][i]['id'])
            number = request.data['listProduct'][i]['number']
            if request.data['listProduct'][i]['product__product_link'] not in all_id_product:
                detail = InvoiceDetail.objects.create(
                    invoice_id=objUpdate.id,
                    product_id=product_attribute_int.product_id,
                    number=number,
                    name_size=request.data['listProduct'][i]['name_size'],
                    name_color=request.data['listProduct'][i]['name_color'],
                    price=request.data['listProduct'][i]['price'],
                )
                detail.save()
                all_id_product.append(request.data['listProduct'][i]['product__product_link'])
            else:
                detail = InvoiceDetail.objects.filter(
                    invoice_id=objUpdate.id,
                    product_id=product_attribute_int.product_id,
                    number=number,
                    name_size=request.data['listProduct'][i]['name_size'],
                    name_color=request.data['listProduct'][i]['name_color'],
                    price=request.data['listProduct'][i]['price'],
                ).first()
                detail.number = detail.number + number
                detail.save()

            product_attribute_int.value = product_attribute_int.value - number
            if product_attribute_int.value < 0:
                err = "totalNumber In Warehouse is out of stock"
                detail.delete()
                objUpdate.delete()
                return err
            product_attribute_int.save()
            total_price = total_price + number * request.data['listProduct'][i]['price']
        if total_price - float(request.data['coupon']) > 0:
            objUpdate.totalPrice = total_price - request.data.get('coupon', 0),
        else:
            objUpdate.totalPrice = 0
        objUpdate.save()
        serializer = InvoiceSerializer(objUpdate)
        try:
            # # notification
            count = Invoice.objects.filter(is_paid=False).count()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'invoice_notification', {
                    'type': 'send.invoice_notification',
                    'value': str(count)
                }
            )
            # user = User.objects.get(id=request.user.id)
            # obj_notification = Notifications()
            # obj_notification.created_by = user
            # obj_notification.notification = "Invoice " + objUpdate.id + " have been created and gateway by " + objUpdate.gateway
            # obj_notification.save()
            # # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def destroy(self, pk):
        object_destroy = Invoice.objects.get(pk=pk)
        object_destroy.delete()
        serializer = InvoiceSerializer(object_destroy, many=False)
        return serializer.data
