from rest_framework import serializers, fields
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = (
            'id',
            'type',
            'name',
            'description',
            'no_of_wheels',
            'price',
            'image',
            'date_added',
            'get_absolute_url',
            'get_image',
        )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'vehicle',
            'quantity'
        )


class OrderSerializer(serializers.ModelSerializer):
    delivery_date = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'vehicles',
            'ordererd_date',
            'delivery_date',
            'ordererd'
        )
