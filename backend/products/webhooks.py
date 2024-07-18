from djstripe import webhooks as djstripe_hooks
from djstripe.models import Subscription
from djstripe.settings import djstripe_settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
import stripe

@djstripe_hooks.handler("checkout.session.completed") # need to handle the checkout session completed event in case the user closes the browser before reaching the callback URL
def handle_checkout_session_completed(event, **kwargs):
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY

    session = event.data.object
    client_reference_id = session.get("client_reference_id")

    user = get_user_model().objects.get(id=client_reference_id)

    subscription = stripe.Subscription.retrieve(session.subscription)
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

    if user.subscription == djstripe_subscription:
        return
    
    user.subscription = djstripe_subscription
    user.customer = djstripe_subscription.customer
    user.save()

    return Response(status=status.HTTP_200_OK)