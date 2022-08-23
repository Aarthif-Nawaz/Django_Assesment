from django.urls import path, include
from coreservice import views


urlpatterns = [
    path('vehicles/', views.VehicleView.as_view()),
    path('cart/',views.CartView.as_view()),
    path('order/', views.OrderView.as_view())
]


