from django.shortcuts import render, get_object_or_404
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

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)

    return render(
        request,
        "cliente/detalle_producto.html",
        {"producto": producto}
    )