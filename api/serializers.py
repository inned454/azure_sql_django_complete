from rest_framework import serializers
from .models import Store, Product


class StoreSerializer(serializers.ModelSerializer):
    # Serializer for Store model
    class Meta:
        model = Store
        fields = ['store_id', 'store_location']


class ProductSerializer(serializers.ModelSerializer):
    # Serializer for Product model
    class Meta:
        model = Product
        fields = '__all__'
