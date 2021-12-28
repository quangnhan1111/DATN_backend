from .models import Coupon
from .repository import CouponRepository


class CouponService():
    def __init__(self):
        self.coupon_repository = CouponRepository()

    def activate(self, pk):
        if Coupon.objects.filter(deleted_at=False, id=pk).exists():
            couponUpdate = Coupon.objects.get(id=pk)
            return self.coupon_repository.activate(couponUpdate)
        return None

    def get_list_no_paginate(self):
        coupons = self.coupon_repository.get_list_no_paginate()
        return coupons

    def index(self):
        coupons = self.coupon_repository.index()
        return coupons

    def store(self, request):
        data = self.coupon_repository.store(request)
        return data

    def show(self, pk):
        if Coupon.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Coupon.objects.filter(deleted_at=False, id=pk).exists():
            return self.coupon_repository.show(pk)
        return None

    def update(self, request, pk):
        if Coupon.objects.filter(deleted_at=False, id=pk).exists():
            couponUpdate = Coupon.objects.get(id=pk)
            return self.coupon_repository.update(couponUpdate, request)
        return None

    def destroy(self, request, pk):
        if Coupon.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Coupon.objects.filter(deleted_at=False, id=pk).exists():
            return self.coupon_repository.destroy(request, pk)
        return None
