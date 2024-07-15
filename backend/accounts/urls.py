from django.urls import path, re_path, include
from allauth.account.views import confirm_email as allauthemailconfirmation
from .views import CustomConfirmEmailView

import regex

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('email_confirmation/(?P<key>{0})/', CustomConfirmEmailView.as_view(), name="account_confirm_email"),
]
