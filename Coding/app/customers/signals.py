from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Customer


@receiver(post_save, sender=Customer)
def create_auth_token_customer(sender, instance, created, **kwargs):
    print(sender)
    # Model.User
    print(instance)
    # testUser
    print(created)
    # true or false
    user = User.objects.get(id=instance.user_id)
    if created:
        Token.objects.create(user=user)
