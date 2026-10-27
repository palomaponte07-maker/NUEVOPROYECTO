from django.shortcuts import render, get_object_or_404
from .models import Producto
from django.utils import timezone
from .models import Producto, Categoria
from django.shortcuts import render

def inicio(request):
    # Consultar productos activos y variantes relacionadas
    productos_destacados = Producto.objects.filter(
        estado=True
    ).prefetch_related("variantes")

    # Verificar si cada producto tiene stock disponible
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

    # Filtrar por categoría si se proporciona en la solicitud GET
    categoria = request.GET.get("categoria")

    # Filtrar productos por categoría si se proporciona
    if categoria:
        productos = productos.filter(
            categoria_id=categoria
        )

    # Disponibilidad, verificar si cada producto tiene stock disponible
    for producto in productos:
        producto.tiene_stock = any(
            variante.stockProducto > 0
            for variante in producto.variantes.all()
        )

    # Obtener todas las categorías para mostrar en la página de productos
    categorias = Categoria.objects.all()

    return render(
        request,
        "cliente/productos.html",
        {
            "productos": productos,
            "categorias": categorias
        }
    )

# Función para mostrar el detalle de un producto específico
def detalle_producto(request, id):
    producto = get_object_or_404(
        Producto,
        idProducto=id,
        estado=True
    )

    # Obtener todas las variantes del producto y sus imágenes
    variantes = producto.variantes.all()
    # Crear una lista para almacenar los datos de las variantes y sus imágenes
    variantes_data = []

    # Recorrer cada variante, obtener sus imágenes y agregarlas a la lista de datos
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

def contacto(request):
    return render(request, 'cliente/contacto.html')