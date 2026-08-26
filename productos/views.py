from django.shortcuts import render, get_object_or_404
from .models import Producto
from django.utils import timezone

def inicio(request):
    productos_destacados = Producto.objects.filter(
        estado=True
    )

    return render(
        request,
        "cliente/inicio.html",
        {"productos_destacados": productos_destacados}
    )

def productos(request):
    productos = Producto.objects.filter(
         estado=True
    )

    return render(
        request,
        "cliente/productos.html",
        {"productos": productos}
    )

def detalle_producto(request, id):
    producto = get_object_or_404(
        Producto,
        idProducto=id,
        estado=True
    )

    variantes = producto.variantes.all()

    colores = variantes.values_list(
        'color',
        flat=True
    ).distinct()

    talles = variantes.values_list(
        'talle',
        flat=True
    ).distinct()

    return render(
        request,
        "cliente/detalle_producto.html",
        {
            "producto": producto,
            "variantes": variantes,
            "colores": colores,
            "talles": talles
        }
    )