from django.db import models

# Create your models here.
from base.models import Base
from customers.models import Customer
from products.models import Product


class Review(Base):
    star = models.PositiveSmallIntegerField()
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()
