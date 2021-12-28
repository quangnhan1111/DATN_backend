from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from base.models import Base


class ChatRoom(Base):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()


class ChatMessage(Base):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    message = models.TextField()

    def delete(self):
        self.deleted_at = True
        self.save()

    def restore(self):
        self.deleted_at = False
        self.save()


