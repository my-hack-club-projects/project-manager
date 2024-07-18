from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings
from django.shortcuts import redirect

from djstripe.models import Product, Price, APIKey
from django.conf import settings
from . import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from djstripe.settings import djstripe_settings
from djstripe.models import Subscription, APIKey

import stripe

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class PriceList(APIView):
    def get(self, request):
        prices = Price.objects.all()
        serializer = serializers.PriceSerializer(prices, many=True)
        return Response(serializer.data)
    
class KeyList(APIView):
    def get(self, request):
        pub_key = djstripe_settings.STRIPE_PUBLIC_KEY

        return Response({
            'public_key': pub_key.secret,
            'pricing_table_id': settings.STRIPE_PRICING_TABLE_ID,
            'client_reference_id': request.user.id
        })
    
class ConfirmPayment(APIView):
    def get(self, request):
        stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY

        session_id = request.GET.get('session_id')

        if not session_id:
            return redirect('/payment/failure')
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.InvalidRequestError:
            return redirect('/payment/failure')
        
        client_reference_id = int(session.client_reference_id)
        user = get_user_model().objects.get(id=client_reference_id)

        if user != request.user:
            return redirect('/payment/failure')

        subscription = stripe.Subscription.retrieve(session.subscription)
        djstripe_subscription = Subscription.sync_from_stripe_data(subscription)

        user.subscription = djstripe_subscription
        user.customer = djstripe_subscription.customer
        user.save()

        return redirect('/payment/success')
    
class IsPremium(APIView):
    def get(self, request):
        user = request.user
        is_premium = user.subscription and user.subscription.status == "active"
        return Response({'is_premium': is_premium})