from rest_framework import serializers
from djstripe.models import Product, Price

class ProductSerializer(serializers.ModelSerializer):
    prices = serializers.SerializerMethodField()

    def get_prices(self, obj):
        return PriceSerializer(obj.prices.all(), many=True).data

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'images',
            'active',
            'prices',
            'metadata',
        ]
        
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            'id',
            'unit_amount',
            'currency',
            'type',
            'recurring',
            'metadata',
            'active',
            'product',
        ]