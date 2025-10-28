from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import jwt

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user = user_to_create.save()

            if user.is_artist:
                from artists.models import Artist
                Artist.objects.create(user=user)

            return Response({
                'message': 'Registration successful',
                'is_artist': user.is_artist
            }, status=status.HTTP_201_CREATED)

        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail='Invalid Credentials')
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail='Invalid Credentials')

        dt = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {
                'sub': str(user_to_login.id), 
                'exp': int(dt.strftime('%s')),
                'id': user_to_login.id,
                'username': user_to_login.username,
                'email': user_to_login.email,
                'is_artist': user_to_login.is_artist,
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return Response({
            'token': token,
            'message': f"Welcome back {user_to_login.username}",
        })
