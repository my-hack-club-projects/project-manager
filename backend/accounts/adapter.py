from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        try:
            email = sociallogin.account.extra_data.get('email')
            verified = sociallogin.account.extra_data.get('verified_email')
            if email and verified:
                user = User.objects.get(email=email)
                if not sociallogin.is_existing:
                    sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass