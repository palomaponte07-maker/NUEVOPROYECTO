from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrito, name='carrito'),

    path(
        'agregar/<int:idProducto>/',
        views.agregar_al_carrito,
        name='agregar_al_carrito'
    ),
]