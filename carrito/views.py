from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from decimal import Decimal

from .models import Carrito, CarritoProducto
from productos.models import Producto, ProductoVariante
from clientes.models import Cliente
from pedidos.views import crear_pedido, agregar_detalle
from administracion.models import Administrador

from administracion.models import Administrador, Notificacion

from django.db import transaction

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

    
    if request.method == "POST" and carrito and productos_carrito:

        metodo_pago = request.POST.get("metodoPago")

        cliente = Cliente.objects.create(
            nombre=request.POST.get("nombre"),
            apellido=request.POST.get("apellido"),
            DNI=request.POST.get("dni"),
            telefono=request.POST.get("telefono"),
            email=request.POST.get("email"),
            calle=request.POST.get("calle"),
            numCalle=request.POST.get("numero"),
            codPostal=request.POST.get("codigoPostal"),
            ciudad=request.POST.get("ciudad"),
            provincia=request.POST.get("provincia")
        )

        administrador = Administrador.objects.first()

        carrito.cliente = cliente
        
        if not carrito.numeroPedido:
            carrito.numeroPedido = carrito.idCarrito

        pedido = crear_pedido(
        cliente_id=cliente.idCliente,
        administrador_id=administrador.idAdministrador,
        numero_pedido=carrito.numeroPedido or str(carrito.idCarrito),
        fecha=timezone.now().date(),
        estado_pago="Pendiente",
        metodo_pago=metodo_pago
        )

        carrito.fecha = timezone.now()
        carrito.estadoPago = "PENDIENTE"
        carrito.metodoPago = metodo_pago
        carrito.save()

        for item in productos_carrito:
            agregar_detalle(
                pedido_id=pedido.idPedido,
                producto_id=item.producto.idProducto,
                cantidad=item.cantidad,
                variante_id=item.variante.idVariante if item.variante else None,
                stock_reservado=True
        )

        Notificacion.objects.create(
            administrador=administrador,
            producto=productos_carrito[0].producto,
            pedido=pedido,
            fecha=timezone.now().date()
        )
        
        carrito.estado = False
        carrito.save()

        
        request.session.pop("idCarrito", None)


        return redirect("carrito")

    subtotal = sum(
        item.subTotal or 0
        for item in productos_carrito
    )

    cantidad = sum(
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

def agregar_al_carrito(request, idProducto):

    print("AGREGAR AL CARRITO EJECUTADO")
    print("METODO:", request.method)
    print("ID PRODUCTO:", idProducto)

    if request.method == "POST":

        producto = get_object_or_404(
            Producto,
            idProducto=idProducto,
            estado=True
        )

        idVariante = request.POST.get("idVariante")

        print("ID VARIANTE:", idVariante)

        variante = get_object_or_404(
            ProductoVariante,
            idVariante=idVariante,
            producto=producto
        )

        # Verificar que haya stock disponible
        if variante.stockProducto <= 0:
            return redirect(
                f"/productos/{producto.idProducto}/?carrito=abierto"
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

        carrito_producto = CarritoProducto.objects.filter(
            carrito=carrito,
            producto=producto,
            variante=variante,
            estado=True
        ).first()

        # Reservar una unidad de stock
        variante.stockProducto -= 1

        # Reposición automática
        if variante.stockProducto <= 3 and variante.stockDeposito > 0:

            cantidad_reponer = min(
                5,
                variante.stockDeposito
            )

            variante.stockProducto += cantidad_reponer
            variante.stockDeposito -= cantidad_reponer

        variante.save(
            update_fields=[
                "stockProducto",
                "stockDeposito"
            ]
        )

        if carrito_producto:

            carrito_producto.cantidad += 1

            carrito_producto.subTotal = (
                carrito_producto.cantidad
                * carrito_producto.precioUnitario
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

        return redirect(
            f"/productos/{producto.idProducto}/?carrito=abierto"
        )

    return redirect(
        f"/productos/{idProducto}/?carrito=abierto"
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

    return redirect("carrito")




@transaction.atomic
def expirar_carritos():
    ahora = timezone.now()

    carritos_expirados = Carrito.objects.filter(
        estado=True,
        fechaExpiracion__lt=ahora
    )

    for carrito in carritos_expirados:

        productos = CarritoProducto.objects.filter(
            carrito=carrito,
            estado=True
        )

        for item in productos:

            if item.variante:

                variante = ProductoVariante.objects.select_for_update().get(
                    idVariante=item.variante_id
                )

                variante.stockProducto += item.cantidad

                variante.save(
                    update_fields=["stockProducto"]
                )

            item.estado = False

            item.save(
                update_fields=["estado"]
            )

        carrito.estado = False

        carrito.save(
            update_fields=["estado"]
        )

@transaction.atomic
def eliminar_del_carrito(request, idCarritoProducto):

    carrito_producto = get_object_or_404(
        CarritoProducto,
        idCarritoProducto=idCarritoProducto,
        estado=True
    )

    variante = carrito_producto.variante

    # Devolver al stock las unidades reservadas
    if variante:
        variante.stockProducto += carrito_producto.cantidad

        variante.save(
            update_fields=["stockProducto"]
        )

    # Marcar el producto del carrito como inactivo
    carrito_producto.estado = False
    carrito_producto.save(
        update_fields=["estado"]
    )

    actualizar_carrito(carrito_producto.carrito)

    return redirect(
        f"/productos/{carrito_producto.producto.idProducto}/?carrito=abierto"
    )


