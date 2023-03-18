from django.db import models
from django.contrib.auth.models import User


class ChatGroup(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='batches')

    def __str__(self):
        return self.name


class Message(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content