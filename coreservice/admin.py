from django.contrib import admin
from .models import User,OrderItem,Order,Vehicles


admin.site.register(User)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Vehicles)

# Register your models here.
