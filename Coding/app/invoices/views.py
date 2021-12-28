import math

from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission
from rolepermissions.permissions import available_perm_status

from app.utils import paginate, response
from invoices.service import InvoiceService


@api_view(['GET'])
@csrf_protect
def getInvoicesByCustomer(request):
    user = request.user
    page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(page)
    invoice_service = InvoiceService()
    if has_permission(user, 'can_view_invoice'):
        invoices = invoice_service.getInvoicesByCustomer()
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, page, math.ceil(count / per_page))
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def getInvoicesByEmployee(request):
    user = request.user
    invoice_service = InvoiceService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    if has_permission(user, 'can_view_invoice'):
        invoices = invoice_service.getInvoicesByEmployee()
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def getInvoicesForOneEmployeeStatus(request, pk):
    user = request.user
    invoice_service = InvoiceService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    if has_permission(user, 'can_view_invoice'):
        invoices = invoice_service.getInvoicesForOneEmployeeStatus(pk)
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def getInvoicesForOneCustomerStatus( request, pk):
    print(available_perm_status(request.user))
    user = request.user
    invoice_service = InvoiceService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    if has_permission(user, 'view_invoice'):
        invoices = invoice_service.getInvoicesForOneCustomerStatus(pk)
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def getInvoicesForEmployeeStatus(request):
    user = request.user
    invoice_service = InvoiceService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    if has_permission(user, 'view_invoice'):
        invoices = invoice_service.getInvoicesForEmployeeStatus()
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@csrf_protect
def getInvoicesForCustomerStatus(request):
    user = request.user
    invoice_service = InvoiceService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    if has_permission(user, 'view_invoice'):
        invoices = invoice_service.getInvoicesForCustomerStatus()
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def showOneInvoices( request, pk):
    user = request.user
    invoice_service = InvoiceService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    if has_permission(user, 'view_invoice'):
        invoices = invoice_service.showOneInvoices(pk)
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@csrf_protect
def showOneInvoicesAndShowEmployee(request, pk):
    user = request.user
    invoice_service = InvoiceService()
    page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(page)
    if has_permission(user, 'view_invoice'):
        invoices = invoice_service.showOneInvoicesAndShowEmployee(pk)
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, page, math.ceil(count / per_page))
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def showOneInvoicesAndShowCustomer(request, pk):
    user = request.user
    invoice_service = InvoiceService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    if has_permission(user, 'view_invoice'):
        invoices = invoice_service.showOneInvoicesAndShowCustomer(pk)
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@csrf_protect
def showInvoicesByIdEmployee( request, pk):
    user = request.user
    invoice_service = InvoiceService()
    page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(page)
    if has_permission(user, 'view_invoice'):
        invoices = invoice_service.showInvoicesByIdEmployee(pk)
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, page, math.ceil(count / per_page))
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@csrf_protect
def showInvoicesByIdCustomer(request, pk):
    user = request.user
    invoice_service = InvoiceService()
    page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(page)
    if has_permission(user, 'view_invoice'):
        invoices = invoice_service.showInvoicesByIdCustomer(pk)
        count = len(invoices)
        content = response(invoices[start:end], 'successfully', True, count, page, math.ceil(count / per_page))
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


class InvoiceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.invoice_service = InvoiceService()

    def post(self, request):
        user = request.user
        print(available_perm_status(request.user))
        if has_permission(user, 'add_invoice'):
            invoice = self.invoice_service.store(request)
            content = response(invoice, 'Payment completed successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_invoice'):
            invoice = self.invoice_service.update(pk, request)
            if invoice is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(invoice, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_invoice'):
            invoice = self.invoice_service.destroy(pk)
            if invoice is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(invoice, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


# class DetailInvoice(APIView):
#     def __init__(self):
#         self.invoice_service = InvoiceService()
#
#     def get(self, request, pk):
#         user = request.user
#         if has_permission(user, 'can_view_invoice'):
#             post = self.invoice_service.show(pk)
#             if post is None:
#                 return Response('NOne')
#             return Response(post)
#         return Response("Unauthorized")
