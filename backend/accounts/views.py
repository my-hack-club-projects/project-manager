from allauth.account.views import ConfirmEmailView
from django.shortcuts import redirect

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.views.decorators.csrf import csrf_exempt

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        self.object = confirmation = self.get_object()
        email_address = confirmation.confirm(self.request)

        if not email_address:
            return self.respond(request, False)
        
        self.logout_other_user(self.object)

        return self.respond(request, True)
    
    def respond(self, request, success):
        scheme = request.scheme
        host = request.get_host()
        base_url = scheme + '://' + host + '/'

        if success:
            return redirect(base_url + 'email_confirm/success')
        else:
            return redirect(base_url + 'email_confirm/fail')
        
class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/accounts/github/login/callback/"
    client_class = OAuth2Client

    def get(self, request, *args, **kwargs):
        request.data['code'] = request.query_params.get('code', '')
        return self.post(request, *args, **kwargs)
    
    def get_response(self):
        return redirect('/')