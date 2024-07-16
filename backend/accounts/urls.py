from django.urls import path, re_path, include
from allauth.account.views import confirm_email as allauthemailconfirmation
from .views import CustomConfirmEmailView, GitHubLogin

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include('allauth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^email_confirmation/(?P<key>.+)/$', CustomConfirmEmailView.as_view(), name="account_confirm_email"),

    path('github/login/callback/', GitHubLogin.as_view(), name='github_login'),
]
