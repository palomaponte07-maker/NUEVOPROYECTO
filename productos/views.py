from django.shortcuts import render
from .models import Producto

def inicio(request):
    productos_destacados = Producto.objects.filter(porcentajeDescuento__gt=0)

    return render(
        request,
        "cliente/inicio.html",
        {"productos_destacados": productos_destacados}
    )

def productos(request):
    productos = Producto.objects.all()

    return render(
        request,
        "cliente/productos.html",
        {"productos": productos}
    )