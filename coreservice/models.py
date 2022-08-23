from django.db import models
from django.conf import settings


# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Vehicles(models.Model): #As a company, I want all my products in a database, so I can offer them via our new platform to customers - add it from addmin or from frontend
    id=models.AutoField(primary_key=True)
    type = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    description = models.TextField()
    license_no = models.CharField(max_length=250)
    no_of_wheels = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.name}/'

    def get_image(self):
        if self.image:
            return 'http://localhost:8000' + self.image.url
        return ''


class OrderItem(models.Model):
    id = models.IntegerField(primary_key=True)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.vehicle.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicles = models.ManyToManyField(OrderItem)
    ordererd_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    ordererd = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "ordererd_date"




