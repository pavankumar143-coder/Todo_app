# from django.shortcuts import render
from .models import User,Todo
from .Serializer import UserSerializer,TodoSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class SignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        mobile = request.data.get("mobile", "")
        username = request.data.get("username","")
        password = request.data.get("password", "")
        user = User.objects.filter(mobile=mobile,username=username, password=password).first()
        if user:
            refresh = RefreshToken.for_user(user)
            response = {"refresh": str(refresh), "access": str(refresh.access_token)}
            return Response(response)
        else:
            return Response({"error": "Invalid mobile,username,or password"}, status=400)

class Pages_Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TodoListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer
    pagination_class = Pages_Pagination

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)