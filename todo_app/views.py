
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from .models import Todo
from .serializers import TodoSerializer, UserSerializer
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login,logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
import logging

@api_view(['POST','GET'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
   
# @api_view(['POST'])
# def login_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(username=username, password=password)
    
#     if user is not None:
#         login(request, user)
        
#         # Get or create a Token for the user
#         token, created = Token.objects.get_or_create(user=user)
        
#         # Prepare user data to be returned in response (if needed)
#         user_data = {
#             'id': user.id,
#             'username': user.username,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'email': user.email,
#         }
        
#         # Return the token and optionally user data in response
#         response_data = {
#             'token': token.key,
#             'user': user_data,  # Include user data if required
#             'message': 'Login successful',
#         }
        
#         return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        
        # Get or create a Token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # Prepare user data to be returned in response (if needed)
        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        
        # Get user's todo tasks
        todos = Todo.objects.filter(user=user)
        todo_serializer = TodoSerializer(todos, many=True)
        
        # Return the token, user data, and todos in response
        response_data = {
            'token': token.key,
            'user': user_data,  # Include user data if required
            'todos': todo_serializer.data,
            'message': 'Login successful',
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)    
@api_view(['POST'])
def logout_view(request):
    # Assuming Token authentication is used
    if request.user.is_authenticated:
        # Delete the user's token
        Token.objects.filter(user=request.user).delete()
        # Logout the user
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'You are not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
# @api_view(['POST'])
# def logout_view(request):
#   # Delete the user's token objects.all()
#     Token.objects.filter(user=request.user).delete()    # Logout the user
#     logout(request)
#     return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
  

logger = logging.getLogger(__name__)
@api_view(["GET", "POST"])
# @login_required
def todo_list(request):
    # if request.method == "GET":
    #     user = request.user
    #     # logger.info(f"GET request received for todos by user: {user}")
    #     todos =Todo.objects.filter(user=user)
    #     serializer = TodoSerializer(todos, many=True)
    #     return Response(serializer.data)
    # if request.method == "GET":
    #     user = request.user  # Get the logged-in user
        
    #     if user.is_authenticated:
    #         todos = Todo.objects.filter(user=user)
    #         serializer = TodoSerializer(todos, many=True)
    #         return Response(serializer.data)
    #     else:
    #         return Response({"error": "User is not authenticated"}, status=401)
    if request.method == "GET":
        username = request.query_params.get('username')  # Get username from query parameters
        if username:
            # Fetch user object based on username
            user = get_object_or_404(User, username=username)
            todos = Todo.objects.filter(user=user)
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Username parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "POST":
        # Assign logged-in user to the todo based on username query parameter
        username = request.query_params.get('username')
        user = get_object_or_404(User, username=username)
        
        # Prepare data to save
        todo_data = {
            'task': request.data.get('task'),  # Assuming task is passed in request data
            'completed': False,  # Assuming initial state of task is not completed
            'user': user.id,  # Assign the logged-in user to the task
            'date_created': timezone.now(),
        }
        
        serializer = TodoSerializer(data=todo_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
    # elif request.method == "POST":
    #     request.data['user'] = request.user.id  # Assign logged-in user to the todo
    #     request.data['date_created'] = timezone.now() 
    #     serializer =TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "PATCH", "DELETE"])    
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, id=pk)

    if request.method == "GET":
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method =="DELETE":
        todo.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
