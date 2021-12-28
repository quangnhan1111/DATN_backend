# Create your views here.
import math

from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission

from app.utils import paginate, response
from products.models import Product, CF
from products.service import ProductService

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
import csv

from reviews.models import Review


@api_view(['GET'])
def RS(request):
    data_base = Review.objects.values_list('customer_id', 'product_id', 'star')
    rate_train = np.array(data_base)
    rate_test = np.array(data_base)
    print(rate_test)

    # indices start from 0
    # rate_train[:, :2] -= 1
    # rate_test[:, :2] -= 1

    rs = CF(rate_test, k=10, uuCF=1)
    rs.fit()

    n_tests = rate_test.shape[0]
    SE = 0  # squared error
    for n in range(n_tests):
        pred = rs.pred(rate_test[n, 0], rate_test[n, 1], normalized=0)
        SE += (pred - rate_test[n, 2]) ** 2
    RMSE = np.sqrt(SE / n_tests)
    print(f'User-user CF, RMSE = {RMSE}')

    return Response(rs.print_recommendation(10), status=status.HTTP_200_OK)


@api_view(['GET'])
def sorted_high_to_low(request):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.sorted_high_to_low()
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def sorted_low_to_high(request):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.sorted_low_to_high()
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_base_price(request, price_min, price_max):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.search_base_price(price_min, price_max)
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_base_review(request, rating):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.search_base_review(rating)
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_base_size(request, name_size):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.search_base_size(name_size)
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_wishlist_product(request, idCustomer, idPro):
    product_service = ProductService()
    if request.method == 'GET':
        check = product_service.check_wishlist_product(idCustomer, idPro)
        content = response(check, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_wishlist_product(request, idCustomer):
    product_service = ProductService()
    user = request.user
    if request.method == 'GET':
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        products = product_service.get_wishlist_product(idCustomer)
        # print(products.product_count)
        count = len(products)
        content = response(products[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    if request.method == 'POST':
        product = product_service.add_wishlist_product(request, idCustomer)
        content = response('Add successfully', 'successfully', True)
        return Response(data=content, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_product_by_search(request, key):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.get_product_by_search(key)
    # print(products.product_count)
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_new_product(request):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.get_new_product()
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_best_product(request):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.get_best_product()
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_related_product_by_brand(request, pk):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.get_related_product_by_brand(pk)
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_related_product_by_subcate(request, pk):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.get_related_product_by_subcate(pk)
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_related_product_by_cate(request, pk):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.get_related_product_by_cate(pk)
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get(request):
    product_service = ProductService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    products = product_service.index()
    count = len(products)
    content = response(products[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_list_no_page(request):
    product_service = ProductService()
    products = product_service.index()
    content = response(products, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


class ProductView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_service = ProductService()

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_product'):
            if Product.objects.filter(deleted_at=False, name=request.data['name']).first():
                return Response('name Product is taken.')
            product = self.product_service.store(request)
            content = response(product, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_product'):
            products = self.product_service.update(request, pk)
            if products is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(products, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_product'):
            product = self.product_service.destroy(request, pk)
            if product is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if product == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(product, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_details(request, pk):
    product_service = ProductService()
    product = product_service.show(pk)
    if product is None:
        content = response(None, 'None Object', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    if product == 'obj destroyed':
        content = response(None, 'Object Destroyed', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    content = response(product, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def activate(request, pk):
    product_service = ProductService()
    product = product_service.activate(pk)
    if product is None:
        content = response(None, 'None Object', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    if product == 'obj destroyed':
        content = response(None, 'Object Destroyed', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    content = response(product, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)

# import numpy as np  # linear algebra
# import pandas as pd
# from IPython.core.interactiveshell import InteractiveShell
#
# InteractiveShell.ast_node_interactivity = "all"
# import math
# # from sklearn.externals import joblib
# import warnings
#
# warnings.simplefilter('ignore')
# # electronics_data = pd.read_csv(
# #     'C:/Users/ADMIN/Desktop/Training/Framework/Django/Vuejs+Django/e-commerce/venv/app/products/ratings_Electronics.csv',
# #     names=['userId', 'productId', 'Rating', 'timestamp'])
# electronics_data = pd.read_csv(
#     'C:/Users/ADMIN/Desktop/Training/Framework/Django/Vuejs+Django/e-commerce/venv/app/products/members.csv',
#     names=['productId', 'userId', 'Rating', 'timestamp'])
# # electronics_data = electronics_data.iloc[:1048576, 0:]
# print(electronics_data)
# electronics_data.drop(['timestamp'], axis=1, inplace=True)
# # print(electronics_data)
# no_of_rated_products_per_user = electronics_data.groupby(by='userId')['Rating'].count().sort_values(ascending=False)
# quantiles = no_of_rated_products_per_user.quantile(np.arange(0, 1.01, 0.01), interpolation='higher')
#
# new_df = electronics_data.groupby("productId").filter(lambda x: x['Rating'].count() >= 1)
#
# new_df1 = new_df.head()
# # print(new_df1)
# ratings_matrix = new_df1.pivot_table(values='Rating', index='userId', columns='productId', fill_value=0)
# X = ratings_matrix.T
# X1 = X
# # print(X1)
# from sklearn.decomposition import TruncatedSVD
#
# SVD = TruncatedSVD(n_components=10)
# # decomposed_matrix = SVD.fit_transform(X)
# # print(decomposed_matrix)
# # correlation_matrix = np.corrcoef(decomposed_matrix)
# # i = "B00000K135"
# # product_names = list(X.index)
# # product_ID = product_names.index(i)
# # # print(product_ID)
# # correlation_product_ID = correlation_matrix[product_ID]
# # Recommend = list(X.index[correlation_product_ID > 0.65])
# #
# # # Removes the item already bought by the customer
# # Recommend.remove(i)
#
#
# # print(Recommend[0:5])
#
#
# @api_view(['GET'])
# def get_rc(request):
#     content = response(electronics_data_test1, 'failure', False)
#     return Response(data=content, status=status.HTTP_200_OK)
#
#     # response = HttpResponse(content_type='text/csv')
#     #
#     # writer = csv.writer(response)
#     # writer.writerow(['productId', 'userId', 'Rating', 'timestamp'])
#     #
#     # for review in Review.objects.all().values_list('customer_id', 'product_id', 'number_of_star'):
#     #     writer.writerow(review)
#     #
#     # response['Content-Disposition'] = 'attachment; filename="members.csv"'
#
#     return response
