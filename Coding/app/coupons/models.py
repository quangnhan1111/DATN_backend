from django.db import models

# Create your models here.
from base.models import Base


class Coupon(Base):
    name = models.CharField(max_length=100)
    time = models.PositiveSmallIntegerField()
    PHAN_TRAM = 'PHAN_TRAM'
    TIEN_MAT = 'TIEN_MAT'
    LOAI_GIAM_GIA = [
        (PHAN_TRAM, 'PHAN_TRAM'),
        (TIEN_MAT, 'TIEN_MAT'),
    ]
    condition = models.CharField(
        max_length=100,
        choices=LOAI_GIAM_GIA,
        default=TIEN_MAT,
    )
    value = models.PositiveIntegerField()
    name_code = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()
