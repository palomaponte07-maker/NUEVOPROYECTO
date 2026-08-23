from django.shortcuts import render, get_object_or_404
from .models import Producto
from django.utils import timezone

def inicio(request):
    ahora = timezone.now()
    productos_destacados = Producto.objects.filter(
        porcentajeDescuento__gt=0,
        fechaInicioDescuento__lte=ahora,
        fechaFinDescuento__gte=ahora,
        estado=True
    )

    return render(
        request,
        "cliente/inicio.html",
        {"productos_destacados": productos_destacados}
    )

def productos(request):
    productos = Producto.objects.all(
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
        estado = True
        )

    return render(
        request,
        "cliente/detalle_producto.html",
        {"producto": producto}
    )