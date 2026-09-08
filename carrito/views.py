from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from decimal import Decimal

from .models import Carrito, CarritoProducto
from productos.models import Producto, ProductoVariante


def carrito(request):

    idCarrito = request.session.get("idCarrito")

    carrito = None
    productos_carrito = []

    if idCarrito:

        carrito = Carrito.objects.filter(
            idCarrito=idCarrito,
            estado=True
        ).first()

        if carrito:

            productos_carrito = CarritoProducto.objects.filter(
                carrito=carrito,
                estado=True
            ).select_related(
                "producto",
                "variante"
            )

    subtotal = sum(
        item.subTotal or 0
        for item in productos_carrito
    )

    cantidad = sum (
        item.cantidad or 0
        for item in productos_carrito
    )

    iva = subtotal * Decimal('0.21')

    total = subtotal + iva

    return render(
        request,
        'cliente/carrito_producto.html',
        {
            'carrito': carrito,
            'productos_carrito': productos_carrito,
            'subtotal': subtotal,
            'cantidad': cantidad,
            'iva': iva,
            'total': total
        }
    )

def actualizar_carrito(carrito):
    productos = CarritoProducto.objects.filter(
    carrito=carrito,
    estado=True
    )

    subtotal = sum(
    item.subTotal or 0
    for item in productos
    )

    cantidad = sum(
    item.cantidad or 0
    for item in productos
    )

    iva = subtotal * Decimal('0.21')

    total = subtotal + iva

    carrito.subTotal = subtotal
    carrito.cantidad = cantidad
    carrito.total = total
    carrito.save()


def agregar_al_carrito(request, idProducto):
    print("AGREGAR AL CARRITO:", request.method)

    if request.method == "POST":

        producto = get_object_or_404(
            Producto,
            idProducto=idProducto,
            estado=True
        )

        idVariante = request.POST.get("idVariante")

        variante = get_object_or_404(
            ProductoVariante,
            idVariante=idVariante,
            producto=producto
        )

        idCarrito = request.session.get("idCarrito")

        if idCarrito:

            carrito = Carrito.objects.filter(
                idCarrito=idCarrito,
                estado=True
            ).first()

        else:

            carrito = None

        if not carrito:

            carrito = Carrito.objects.create(
                cliente=None,
                fechaCreacion=timezone.now(),
                fechaExpiracion=timezone.now() + timezone.timedelta(hours=24),
                estado=True
            )

            request.session["idCarrito"] = carrito.idCarrito
            print("CARRITO CREADO:", carrito.idCarrito)

        carrito_producto = CarritoProducto.objects.filter(
            carrito=carrito,
            producto=producto,
            variante=variante,
            estado=True
        ).first()

        if carrito_producto:

            carrito_producto.cantidad += 1

            carrito_producto.subTotal = (
                carrito_producto.cantidad *
                carrito_producto.precioUnitario
            )

            carrito_producto.save()

        else:

            precio = producto.precioVenta

            CarritoProducto.objects.create(
                carrito=carrito,
                producto=producto,
                variante=variante,
                cantidad=1,
                precioUnitario=precio,
                subTotal=precio,
                estado=True
            )

        actualizar_carrito(carrito)


        print("PRODUCTO AGREGADO AL CARRITO:", producto.nombre)
        return redirect(
            f"/productos/{producto.idProducto}/?carrito=abierto"    
        )

    return redirect(
    f"/productos/{producto.idProducto}/?carrito=abierto"
    )

def modificar_cantidad(request, idCarritoProducto, accion):

    carrito_producto = get_object_or_404(
        CarritoProducto,
        idCarritoProducto=idCarritoProducto,
        estado=True
    )

    if accion == "sumar":
        carrito_producto.cantidad += 1

    elif accion == "restar":
        if carrito_producto.cantidad > 1:
            carrito_producto.cantidad -= 1

    carrito_producto.subTotal = (
        carrito_producto.cantidad *
        carrito_producto.precioUnitario
    )

    carrito_producto.save()
    actualizar_carrito(carrito_producto.carrito)

    return redirect(
        f"/productos/{carrito_producto.producto.idProducto}/?carrito=abierto"
    )

def eliminar_del_carrito(request, idCarritoProducto):

    carrito_producto = get_object_or_404(
        CarritoProducto,
        idCarritoProducto=idCarritoProducto,
        estado=True
    )

    carrito_producto.estado = False
    carrito_producto.save()

    return redirect(
    f"/productos/{carrito_producto.producto.idProducto}/?carrito=abierto"
    )