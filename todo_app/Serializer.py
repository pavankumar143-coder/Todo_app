from rest_framework import serializers
from .models import User, Todo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'owner', 'task', 'due_date', 'completed']
