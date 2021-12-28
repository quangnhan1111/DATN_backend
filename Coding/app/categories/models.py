from django.db import models

# Create your models here.
from base.models import Base


class Category(Base):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()
