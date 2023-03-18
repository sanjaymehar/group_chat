from rest_framework import serializers

from .models import ChatGroup, Message


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = ('id', 'name', 'users')


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ('id', 'group', 'sender', 'content', 'timestamp')
