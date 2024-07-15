from dj_rest_auth.registration.views import RegisterView
from allauth.account.views import ConfirmEmailView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomRegisterSerializer, ConfirmEmailSerializer, SetPasswordSerializer
from django.contrib.auth.models import User

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.kwargs['key'] = self.request.query_params.get('key', '')
        return super().get(*args, **kwargs)

class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password1'])
        request.user.save()
        return Response({"detail": "Password has been set."})
