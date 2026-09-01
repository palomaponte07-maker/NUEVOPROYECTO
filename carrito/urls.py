from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrito, name='carrito'),

    path(
        'agregar/<int:idProducto>/',
        views.agregar_al_carrito,
        name='agregar_al_carrito'
    ),

    path(
        'modificar/<int:idCarritoProducto>/<str:accion>/',
        views.modificar_cantidad,
        name='modificar_cantidad'
    ),

    path(
        'eliminar/<int:idCarritoProducto>/',
        views.eliminar_del_carrito,
        name='eliminar_del_carrito'
    ),
]