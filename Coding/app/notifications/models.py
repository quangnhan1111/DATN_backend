import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import models

from base.models import Base
from customers.serializer import UserSerializer


class Notifications(Base):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.TextField(max_length=100)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        serializer = UserSerializer(data={
            'username': self.created_by.username,
            'email': self.created_by.email,
            'password': self.created_by.password,
            'last_name': self.created_by.last_name,
            'first_name': self.created_by.first_name,
        })
        serializer.is_valid(raise_exception=True)

        super(Notifications, self).save(*args, **kwargs)
        data = {
            'id': self.id,
            'created_by': serializer.data,
            'notification': self.notification,
            'is_seen': self.is_seen,
        }
        async_to_sync(channel_layer.group_send)(
            'notification', {
                'type': 'send.notification',
                'value': json.dumps(data)
            }
        )

    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()


class MessageNotifications(Base):
    notification = models.TextField(max_length=100)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        super(MessageNotifications, self).save(*args, **kwargs)
        data = {
            'id': self.id,
            'notification': self.notification,
            'is_seen': self.is_seen,
        }
        async_to_sync(channel_layer.group_send)(
            'message_notification', {
                'type': 'send.message_notification',
                'value': json.dumps(data)
            }
        )


    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()
