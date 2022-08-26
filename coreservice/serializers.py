from rest_framework import serializers, fields
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'password'
        )
        model = User


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Vehicles



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'vehicle',
            'quantity'
        )
        model = OrderItem



class OrderSerializer(serializers.ModelSerializer):
    delivery_date = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        fields = (
            'id',
            'user',
            'vehicles',
            'ordererd_date',
            'delivery_date',
            'ordererd'
        )
        model = Order
