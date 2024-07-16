from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings

from djstripe.models import Product, Price, APIKey
from django.conf import settings
from . import serializers

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
        pub_key = APIKey.objects.get(name='STRIPE_TEST_PUBLIC_KEY')

        return Response({'public_key': pub_key.secret, 'pricing_table_id': settings.STRIPE_PRICING_TABLE_ID})