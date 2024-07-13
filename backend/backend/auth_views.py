from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class UserLoginAPIView(APIView):
    """
    View to log in a user.
    """
    def get(self, request):
        # check if user is already logged in
        if request.user.is_authenticated:
            return JsonResponse({'message': 'User is already logged in', 'authenticated': True}, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'User is not logged in', 'authenticated': False}, status=status.HTTP_200_OK)
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Logged in successfully', 'authenticated': True}, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'Invalid credentials', 'authenticated': False}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    """
    View to log out a user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Logged out successfully', 'authenticated': False}, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):
    """
    View to get user profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,

            "defaut_category": 1, # user.default_category,
            "archive_category": 2, # user.archive_category,
        }
        return Response(data, status=status.HTTP_200_OK)