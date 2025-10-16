from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from .serializers import UserSerializer
import jwt

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        print('USER CREATE', user_to_create)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_202_ACCEPTED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        