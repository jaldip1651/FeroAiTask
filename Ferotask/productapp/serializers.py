from rest_framework import serializers
from .models import Customer, Product, Order, Order_Item


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
        }

    def validate_name(self, value):
        if Customer.objects.filter(name=value).exists():
            raise serializers.ValidationError("Customer with this name already exists")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []}
        }

    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError("Product with this name already exists")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        # depth = 2
