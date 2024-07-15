from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):

        """
            Changing the confirmation URL to fit the domain that we are working on
        """

        running_url = request.get_host()
        scheme = request.scheme

        url = (
            scheme + "://"
            + running_url
            + "/email_confirmation/"
            + emailconfirmation.key
        )

        return url