# from django.shortcuts import render
from .models import User,Todo
from django.http import HttpResponse
from .Serializer import UserSerializer,TodoSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
# Create your views here.

class SignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        mobile = request.data.get("mobile")
        user_name = request.data.get("username")
        password = request.data.get("password")
        if not mobile or not user_name or not password:
            return Response({"error": "Please provide all required data"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            mobile=mobile, username=user_name
        )
        user.set_password(password)
        user.save()
        
        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        return Response({"error": "Could not create user"}, status=400)



class LoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        mobile = request.data.get("mobile")
        username = request.data.get("username")
        password = request.data.get("password")
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
    authentication_classes=[JWTAuthentication]
    serializer_class = TodoSerializer
    pagination_class = Pages_Pagination
    def list(self,request,*args,**kwargs):
        queryset = Todo.objects.all()
        # due_date = self.request.query_params.get('due_date')
        # completed = self.request.query_params.get('completed')
        due_date = request.GET.get('due_date')
        completed = request.GET.get('completed')
        if due_date:
            queryset = queryset.filter(owner=self.request.user,due_date=due_date)
            serializer = self.get_serializer(queryset,many=True) 

        elif completed:
            queryset = queryset.filter(owner=self.request.user,completed=completed)
            serializer = self.get_serializer(queryset,many=True) 

        else:
            queryset = Todo.objects.all()
            queryset = queryset.filter(owner=self.request.user)
            serializer = self.get_serializer(queryset,many=True)
        
        return Response( serializer.data,status=status.HTTP_200_OK) 
    # def get_queryset(self):
    #     return Todo.objects.filter(owner=self.request.user)


class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes =[JWTAuthentication]
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)