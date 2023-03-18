
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import ChatGroup
from .serializer import ChatGroupSerializer


# Create your views here.
class ChatGroupList(generics.ListCreateAPIView):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
    permission_classes = [permissions.IsAuthenticated]