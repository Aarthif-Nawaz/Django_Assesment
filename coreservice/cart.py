import json
from decimal import Decimal
from django.conf import settings
from django.core import serializers

from .models import Vehicles
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

    def get_vehicles(self):
        product_ids = self.cart.keys()
        products = Vehicles.objects.filter(id__in=product_ids)
        for product in products:
            prod = serializers.serialize("json", Vehicles.objects.filter(id=product.id))
            self.cart[str(product.id)]['product'] = json.loads(prod)

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

        return self.cart

    def view(self):
        print(self.cart)

    def action(self, product=None, quantity=1, update_quantity=False, remove=False, view=False):
        if view:
            self.save()
            print(self.cart)
            return self.get_vehicles()
        if remove:
            self.remove(product)
        else:
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0,
                                         'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity

        self.save()
        print(self.cart)

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Vehicles.objects.filter(id__in=product_ids)
        for product in products:
            prod = serializers.serialize("json", Vehicles.objects.filter(id=product.id))
            self.cart[str(product.id)]['product'] = json.loads(prod)

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        return self.cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
