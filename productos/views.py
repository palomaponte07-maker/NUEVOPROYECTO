from django.shortcuts import render, get_object_or_404
from .models import Producto
from django.utils import timezone
from .models import Producto, Categoria

def inicio(request):
    productos_destacados = Producto.objects.filter(
        estado=True
    ).prefetch_related("variantes")

    for producto in productos_destacados:
        producto.tiene_stock = any(
            variante.stockProducto > 0
            for variante in producto.variantes.all()
        )

    categorias = Categoria.objects.all()

    return render(
        request,
        "cliente/inicio.html",
        {
            "productos_destacados": productos_destacados,
            "categorias": categorias
        }
    )

def productos(request):
    productos = Producto.objects.filter(
        estado=True
    ).prefetch_related("variantes")

    categoria = request.GET.get("categoria")

    if categoria:
        productos = productos.filter(
            categoria_id=categoria
        )

    for producto in productos:
        producto.tiene_stock = any(
            variante.stockProducto > 0
            for variante in producto.variantes.all()
        )

    categorias = Categoria.objects.all()

    return render(
        request,
        "cliente/productos.html",
        {
            "productos": productos,
            "categorias": categorias
        }
    )

def detalle_producto(request, id):
    producto = get_object_or_404(
        Producto,
        idProducto=id,
        estado=True
    )

    variantes = producto.variantes.all()
    variantes_data = []

    for variante in variantes:
        imagenes = []

        for imagen in variante.imagen_set.all():

            if imagen.imagen:
                imagenes.append(imagen.imagen.url)

        variantes_data.append({
            'idVariante': variante.idVariante,
            'color': variante.color,
            'talle': variante.talle,
            'stockProducto': variante.stockProducto,
            'imagenes': imagenes
        })

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
            "variantes_data": variantes_data,
            "colores": colores,
            "talles": talles
        }
    )