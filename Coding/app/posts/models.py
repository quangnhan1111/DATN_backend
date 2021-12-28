from django.db import models

# Create your models here.
from base.models import Base


class Post(Base):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_name = models.CharField(max_length=100)
    image_link = models.URLField(max_length=500)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()
