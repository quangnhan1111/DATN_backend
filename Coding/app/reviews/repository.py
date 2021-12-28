from django.db.models import F

from .models import Review
from .serializer import ReviewSerializer


class ReviewRepository:
    def __init__(self):
        pass

    def get_good_review(self):
        reviews = Review.objects.filter(star__gte=3, star__lte=5).order_by('-star')[0:4]\
            .values()
        # serializer = ReviewSerializer(data=list(reviews), many=True)
        # serializer.is_valid(raise_exception=True)
        return [reviews, reviews.count()]

    def get_all_review_by_product(self, pk):
        reviews = Review.objects.filter(product_id=pk, product__deleted_at=False).order_by('id').annotate(
            ProductName=F('product__name'),
            UserName=F('customer__user__username'),
            email=F('customer__user__email')) \
            .values('id', 'star', 'content', 'created_at', 'UserName', 'email', 'ProductName',)
        print(reviews.query)
        return [reviews, reviews.count()]

    def index(self):
        reviews = Review.objects.filter(product__deleted_at=False).order_by('id').annotate(
            ProductName=F('product__name'),
            UserName=F('customer__user__username'),
            email=F('customer__user__email')) \
            .values('id', 'star', 'content', 'created_at', 'ProductName', 'UserName', 'email', 'product_id', 'customer_id')

        return reviews

    def show(self, pk):
        review = Review.objects.filter(id=pk).order_by('id').annotate(
            ProductName=F('product__name'),
            UserName=F('customer__user__username'),
            email=F('customer__user__email')) \
            .values('id', 'star', 'content', 'created_at', 'ProductName', 'UserName', 'email')
        return review

    def store(self, request):
        context = {'request': request}
        serializer = ReviewSerializer(data={
            'star': request.data['star'],
            'content': request.data['content'],
            'product': request.data['product_id'],
            'customer': request.data['user_id'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        serializer = ReviewSerializer(instance=objUpdate, data={
            'star': request.data['star'],
            'content': request.data['content'],
            'product': request.data['product'],
            'customer': request.data['customer'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def destroy(self, request, pk):
        print('sad')
        objDestroy = Review.objects.get(id=pk)
        objDestroy.delete()
        serializer = ReviewSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        return serializer.data

