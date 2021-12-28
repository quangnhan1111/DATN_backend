from django.contrib import admin

# Register your models here.
from invoices.models import Invoice

admin.site.register(Invoice)