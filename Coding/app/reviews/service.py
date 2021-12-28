from reviews.models import Review
from reviews.repository import ReviewRepository


class ReviewService:
    def __init__(self):
        self.review_repository = ReviewRepository()

    def get_good_review(self):
        review = self.review_repository.get_good_review()
        return review

    def get_all_review_by_product(self, pk):
        review = self.review_repository.get_all_review_by_product(pk)
        return review

    def index(self):
        review = self.review_repository.index()
        return review

    def store(self, request):
        data = self.review_repository.store(request)
        return data

    def show(self, pk):
        if Review.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Review.objects.filter(deleted_at=False, id=pk).exists():
            return self.review_repository.show(pk)
        return None

    def update(self, request, pk):
        if Review.objects.filter(deleted_at=False, id=pk).exists():
            objUpdate = Review.objects.get(id=pk)
            return self.review_repository.update(objUpdate, request)
        return None

    def destroy(self, request, pk):
        if Review.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Review.objects.filter(deleted_at=False, id=pk).exists():
            return self.review_repository.destroy(request, pk)
        return None


