from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from base.models import Base
from customers.models import Customer
from staffs.models import Staff


class Invoice(Base):
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?84?\d{9,15}$',
                message="Phone number must be entered in the format '+8423456789'. Up to 15 digits allowed."
            ),
        ],
    )
    full_name = models.CharField(max_length=200)
    message = models.TextField()
    totalPrice = models.DecimalField(max_digits=8, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    is_paid = models.BooleanField(default=False, blank=True, null=True)
    gateway = models.CharField(max_length=100)
    # coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()

