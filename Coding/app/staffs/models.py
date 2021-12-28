from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from base.models import Base


class Staff(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
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
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()