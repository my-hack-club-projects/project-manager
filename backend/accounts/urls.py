from django.urls import path, include
from .views import CustomRegisterView, CustomConfirmEmailView, SetPasswordView

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='account_register'),
    path('email-confirm/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('set-password/', SetPasswordView.as_view(), name='account_set_password'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
]
