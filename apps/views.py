from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
# Create your views here.

class UserListCreateView(APIView):
    def get(self, request):
        

    def patch(self, request):
        