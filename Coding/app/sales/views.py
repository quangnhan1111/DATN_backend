import math

from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rolepermissions.checkers import has_permission
from rolepermissions.permissions import available_perm_status

from app.utils import response, paginate
from sales.service import SaleService


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_totel_user(request):
    user = request.user
    sale_service = SaleService()
    # print(available_perm_status(request.user))
    if has_permission(user, 'view_sale'):
        [totalCustomer, totalEmployee] = sale_service.get_totel_user()
        res = {
            'totalCustomer': totalCustomer,
            'totalEmployee': totalEmployee
        }
        content = response(res, 'successfully', True,)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_total_product_sold_out(request):
    user = request.user
    sale_service = SaleService()
    if has_permission(user, 'view_sale'):
        total = sale_service.get_total_product_sold_out()
        res = {
            'total_product_sold_out': total,
        }
        content = response(res, 'successfully', True,)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_sale_figure_by_day(request):
    user = request.user
    sale_service = SaleService()
    if has_permission(user, 'view_sale'):
        sale_by_day = sale_service.get_sale_figure_by_day()
        res = []
        for item in sale_by_day:
            res.append({
                'total_sale': item['total_sale'],
                'date': str(item['Day'])+'/'+str(item['Month'])+"/"+str(item["Year"]),
                'Day': str(item['Day']),
                'Month': str(item['Month']),
                'Year': str(item["Year"]),
            })
        content = response(res, 'successfully', True,)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_sale_figure_by_month(request):
    print(available_perm_status(request.user))
    user = request.user
    sale_service = SaleService()
    if has_permission(user, 'view_sale'):
        sale_by_day = sale_service.get_sale_figure_by_month()
        print(sale_by_day)
        res = []
        for item in sale_by_day:
            res.append({
                'total_sale': item['total_sale'],
                'date': str(item['Month']) + "/" + str(item["Year"]),
                'Month': str(item['Month']),
                'Year': str(item["Year"]),
            })
        content = response([res], 'successfully', True, )
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_sale_figure_by_staff(request):
    user = request.user
    sale_service = SaleService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    if has_permission(user, 'view_sale'):
        data = sale_service.get_sale_figure_by_staff()
        count = len(data)
        content = response(data[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)




