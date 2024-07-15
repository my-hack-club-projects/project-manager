from dj_rest_auth.registration.views import RegisterView
from allauth.account.views import ConfirmEmailView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomRegisterSerializer, ConfirmEmailSerializer, SetPasswordSerializer
from django.contrib.auth.models import User
from django.shortcuts import redirect

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        self.object = confirmation = self.get_object()
        email_address = confirmation.confirm(self.request)

        if not email_address:
            return self.respond(False)
        
        self.logout_other_user(self.object)

        return self.respond(True)
    
    def respond(self, success):
        if success:
            return redirect('http://localhost:8000/email_confirmed')
        else:
            return redirect('http://localhost:8000/email_not_confirmed')