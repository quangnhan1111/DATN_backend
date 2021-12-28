# Create your views here.
import math

from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission
from rolepermissions.permissions import available_perm_status

from app.utils import paginate, response
from reviews.service import ReviewService


@api_view(['GET'])
def get_all_review_by_product(request, pk):
    review_service = ReviewService()
    page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(page)
    [reviews, count] = review_service.get_all_review_by_product(pk)
    content = response(reviews[start:end], 'successfully', True, count, page, math.ceil(count / per_page))
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@csrf_protect
def get_good_review(request):
    review_service = ReviewService()
    [reviews, count] = review_service.get_good_review()
    content = response(reviews, 'successfully', True, count)
    return Response(data=content, status=status.HTTP_200_OK)


class ReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.review_service = ReviewService()

    def get(self, request):
        user = request.user
        print(available_perm_status(request.user))
        # current_page = int(request.GET.get('page', 1))
        # [start, end, per_page] = paginate(current_page)
        reviews = self.review_service.index()
        content = response(reviews, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        reviews = self.review_service.store(request)
        content = response(reviews, 'successfully', True)
        return Response(data=content, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_review'):
            reviews = self.review_service.update(request, pk)
            if reviews is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(reviews, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        print(request.user)
        print(available_perm_status(request.user))
        if has_permission(user, 'delete_review'):
            review = self.review_service.destroy(pk)
            if review == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(review, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        return Response("Unauthorized")


@api_view(['GET'])
def get_details(request, pk):
    review_service = ReviewService()
    user = request.user
    review = review_service.show(pk)
    if review is None:
        content = response(None, 'None Object', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    if review == 'obj destroyed':
        content = response(None, 'Object Destroyed', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    content = response(review, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)
