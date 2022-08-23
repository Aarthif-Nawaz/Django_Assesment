import random
from django.shortcuts import get_object_or_404
from .models import User, Vehicles, Order
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VehicleSerializer, OrderItemSerializer, OrderSerializer
from .cart import Cart


class VehicleView(APIView):
    def get(self, request, format=None):
        vehicle_id = request.GET.get('vehicle_id')
        if vehicle_id:
            vehicle = Vehicles.objects.filter(id=vehicle_id)
            if len(vehicle) > 0 :
                serialzer = VehicleSerializer(vehicle)
                return Response(serialzer.data,
                                status=status.HTTP_200_OK)  # As a client, I want to view the details of a product, so I can see if the product satisfies my needs
            else:
                return Response({'Error': 'Vehicle Does Not Exist!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            vehicles = Vehicles.objects.all()
            serializer = VehicleSerializer(vehicles, many=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)  # As a client, I want to see an overview of all the products, so I can choose which product I want


class CartView(APIView):

    def get(self, request, format=None):
        cart = Cart(request)
        get_vehicles = cart.get_vehicles()
        return Response({'data':get_vehicles}, status=status.HTTP_200_OK)

    # As a client, I want to add a product to my shopping cart, so I can order it at a later stage
    def post(self, request, format=None):
        data = request.data
        vehicle = get_object_or_404(Vehicles,id=data.get('vehicle_id'))
        if vehicle is not None:
            cart = Cart(request)
            cart.action(product=vehicle)
        return Response({'Success' : 'Successfully Added To Cart'}, status=status.HTTP_200_OK)

    # Update Quantity
    def put(self, request, format=None):
        data = request.data
        vehicle = get_object_or_404(Vehicles,id=request.GET.get('vehicle_id'))
        if vehicle is not None:
            quantity = data.get('quantity')
            cart = Cart(request)
            cart.action(product=vehicle, quantity=quantity, update_quantity=True)
        return Response({'Success': 'Successfully Updated Cart'}, status=status.HTTP_200_OK)

    # As a client, I want to remove a product from my shopping cart, so I can tailor the order to what I actually need
    def delete(self, request, format=None):
        vehicle = get_object_or_404(Vehicles,id=request.GET.get('vehicle_id'))
        if vehicle is not None:
            cart = Cart(request)
            cart.action(product=vehicle,remove=True)
        return Response({'Success': 'Successfully Remove From Cart'}, status=status.HTTP_200_OK)

class OrderView(APIView):

    def get(self, request,format=None):
        order_id = request.GET.get('order_id')
        if order_id:
            order = Order.objects.filter(id=order_id)
            if len(order) > 0 :
                serialzer = OrderSerializer(order)
                return Response(serialzer.data,
                                status=status.HTTP_200_OK)
            else:
                return Response({'Error': 'Order Does Not Exist!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)

    # As a client, I want to order the current contents in my shopping cart, so I can receive the products I need to repair my car
    def post(self, request, format=None):
        cart = Cart(request)
        get_vehicles = cart
        data_request_body = request.data
        total = 0
        order_items = []
        for v in get_vehicles:
            print(v['product'][0]['pk'])
            total += v['total_price']
            try:
                id = random.getrandbits(16)
                data = {
                    'id': id,
                    'vehicle': v['product'][0]['pk'],
                    'quantity': v['quantity']
                }
                serializer = OrderItemSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    order_items.append(id)
            except Exception as e:
                return Response({"Errors": "Some field miss check and enter", "exception": str(e), "status": False},
                                status=status.HTTP_400_BAD_REQUEST)
        order_data = {
            'user':1, # Just for the testcase -  didn't do authentication
            'vehicles': order_items,
            'delivery_date': data_request_body.get('delivery_date'), # As a client, I want to select a delivery date and time, so I will be there to receive the order
            'ordererd': True
        }
        try:
            serializer = OrderSerializer(data=order_data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Success': 'Successfully Registered Order'}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Errors": "Some field miss check, please re enter", "exception": str(e), "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
