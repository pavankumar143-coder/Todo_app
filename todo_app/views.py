# from django.shortcuts import render
from .models import User,Todo
from .Serializer import UserSerializer
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer





