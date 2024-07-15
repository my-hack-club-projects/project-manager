from django.urls import path, re_path, include
from allauth.account.views import confirm_email as allauthemailconfirmation
# from .views import CustomRegisterView, CustomConfirmEmailView, SetPasswordView

import regex

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('rest-auth/registration/account-confirm-email/(?P<key>{0})/', allauthemailconfirmation, name="account_confirm_email"),
]
