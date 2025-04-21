from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description',
                  'inventory', 'price', 'price_with_tax', 'collections']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    collections = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all())

    def calculate_tax(self, product):
        return product.price * Decimal(1.1)
