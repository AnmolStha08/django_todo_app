
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password','email', 'first_name', 'last_name')
        # fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     confirmpassword = serializers.CharField(write_only=True)  # Add a confirmation field
    
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'confirmpassword', 'email', 'first_name', 'last_name')
    
#     def validate(self, data):
#         if data.get('password') != data.get('confirmpassword'):
#             raise serializers.ValidationError("Passwords do not match")
#         return data
    
#     def create(self, validated_data):
#         validated_data.pop('confirmpassword')  # Remove confirmpassword from validated_data
#         user = User.objects.create_user(**validated_data)
#         return user    

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "task", "completed", "created","updated","user"]