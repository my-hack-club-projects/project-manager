from allauth.account.views import ConfirmEmailView
from django.shortcuts import redirect

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
            return redirect(base_url + 'email_confirmed')
        else:
            return redirect(base_url + 'email_not_confirmed')