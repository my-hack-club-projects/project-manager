from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user is already registered with this e-mail address.")
        
        return email

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user

class ConfirmEmailSerializer(serializers.Serializer):
    key = serializers.CharField()

class SetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
