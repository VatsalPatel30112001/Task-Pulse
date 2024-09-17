from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from machines.consumers import *
from .models import *

class SignUp(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username', "")
            password = request.data.get('password', "")
            role = request.data.get('role', "Operator")
            
            if not username or not password:
                return JsonResponse({
                    'status': 'fail',
                    'message': 'Username or Password is not defined.'
                }, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': 'fail',
                    'message': 'Username already exists.'
                }, status=400)
            
            user = User(username=username)
            user.set_password(password)  
            user.save()

            Role.objects.create(user=user, role=role)

            token, created = Token.objects.get_or_create(user=user)

            return JsonResponse({
                'status': 'success',
                'token': token.key,
                'username': user.username,
                'role': role
            }, status=201)

        except:
            return JsonResponse({
                    'status': 'fail',
                    'message': 'Something went wrong.'
                }, status=500)

class Login(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', "")
        password = request.data.get('password', "")
        
        broadcast_data(f'{username} logged in.')
        
        if not username or not password:
                return JsonResponse({
                    'status': 'fail',
                    'message': 'Username or Password is not defined.'
                }, status=400)

        user = authenticate(request, username=username, password=password)    
        
        if user is not None:
            role_obj = Role.objects.get(user=user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'status': 'success',
                'token': token.key, 
                'message': 'User authenticated successfully',
                'role': role_obj.role
            }, status=200)
        else:
            return JsonResponse({'status': 'fail', 'message': 'Invalid username or password'}, status=404)