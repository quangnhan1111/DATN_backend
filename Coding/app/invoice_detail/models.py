from django.db import models

# Create your models here.
from invoices.models import Invoice
from products.models import Product


class InvoiceDetail(models.Model):
    number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    name_color = models.CharField(max_length=100)
    name_size = models.CharField(max_length=100)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)




