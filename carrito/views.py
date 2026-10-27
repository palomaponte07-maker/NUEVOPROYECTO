from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from decimal import Decimal

from pedidos.models import Pedido

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
    # Expira los carritos que han pasado su fecha de expiración y devuelve el stock de los productos
    expirar_carritos()

    # Obtiene el id del carrito de la sesión del usuario
    idCarrito = request.session.get("idCarrito")

    # Inicializa las variables en caso de que no haya un carrito activo
    carrito = None
    productos_carrito = []

    if idCarrito:
        # Busca el carrito activo en la base de datos
        carrito = Carrito.objects.filter(
            idCarrito=idCarrito,
            estado=True
        ).first()

        if carrito:
            # Obtiene los productos del carrito activo y sus variantes, si existen
            productos_carrito = CarritoProducto.objects.filter(
                carrito=carrito,
                estado=True
            ).select_related(
                "producto",
                "variante"
            )

    # Se ejecuta cuando cumple la condición de que el método sea POST y que haya un carrito activo con productos
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
        
        ultimo_pedido = Pedido.objects.order_by('-idPedido').first()

        if ultimo_pedido:
            nuevo_numero = int(ultimo_pedido.numeroPedido) + 1
        else:
            nuevo_numero = 1
            
        pedido = crear_pedido(
        cliente_id=cliente.idCliente,
        administrador_id=administrador.idAdministrador,
        numero_pedido=str(nuevo_numero),
        fecha=timezone.now().date(),
        estado_pago="Pendiente",
        metodo_pago=metodo_pago
        )

        carrito.fecha = timezone.now()
        carrito.estadoPago = "Pendiente"
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
        #verififca que hay stock 
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


        #repone hasta cinco unidades, sin retirar más de las que hay en depósito.
        variante.stockProducto -= 1


        if variante.stockProducto <= 3 and variante.stockDeposito > 0:

            cantidad_reponer = min(
                5,
                variante.stockDeposito
            )

            variante.stockProducto += cantidad_reponer
            variante.stockDeposito -= cantidad_reponer

        # Guardar los cambios en la BD
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



@transaction.atomic
def modificar_cantidad(request, idCarritoProducto, accion):
    
    carrito_producto = get_object_or_404(
        CarritoProducto.objects.select_for_update(),
        idCarritoProducto=idCarritoProducto,
        estado=True
    )

    # Comprobar que el artículo pertenece al carrito de esta sesión
    idCarrito = request.session.get("idCarrito")

    if carrito_producto.carrito_id != idCarrito:
        return redirect("carrito")

    variante = carrito_producto.variante

    if not variante:
        return redirect("carrito")

    variante = ProductoVariante.objects.select_for_update().get(
        idVariante=variante.idVariante
    )

    #Primero verifica que haya stock. 
    # Si hay, descuenta una unidad disponible y aumenta la cantidad del carrito.
    if accion == "sumar":
     
        if variante.stockProducto <= 0:
            return redirect(
                f"/productos/{carrito_producto.producto.idProducto}/?carrito=abierto&error=sin_stock"
            )

        
        variante.stockProducto -= 1
        variante.save(update_fields=["stockProducto"])

        carrito_producto.cantidad += 1

    elif accion == "restar":
        if carrito_producto.cantidad > 1:
            # Devolver una unidad al stock disponible
            variante.stockProducto += 1
            variante.save(update_fields=["stockProducto"])

            carrito_producto.cantidad -= 1

    else:
        return redirect("carrito")
    #actualiza el subtotal del producto y los totales del carrito
    carrito_producto.subTotal = (
        carrito_producto.cantidad *
        carrito_producto.precioUnitario
    )

    carrito_producto.save(update_fields=["cantidad", "subTotal"])

    actualizar_carrito(carrito_producto.carrito)

    return redirect(
        f"/productos/{carrito_producto.producto.idProducto}/?carrito=abierto"
    )


@transaction.atomic
def expirar_carritos():
    ahora = timezone.now()
    # Buscar carritos activos y expirados y devolver el stock de los productos
    carritos_expirados = Carrito.objects.filter(
        estado=True,
        fechaExpiracion__lt=ahora
    )

    for carrito in carritos_expirados:
        #busca los productos de cada carrito
        productos = CarritoProducto.objects.filter(
            carrito=carrito,
            estado=True
        )

        for item in productos:

            if item.variante:
                #debuelve las unidades al stock
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

        #desactiva el carrito expirado
        carrito.estado = False

        carrito.save(
            update_fields=["estado"]
        )

@transaction.atomic
def eliminar_del_carrito(idCarritoProducto):

    #Busca el producto del carrito y lo bloquea para evitar conflictos de concurrencia
    carrito_producto = get_object_or_404(
        CarritoProducto.objects.select_for_update(),
        idCarritoProducto=idCarritoProducto,
        estado=True
    )
    # Obtiene la variante asociada al producto del carrito, si existe
    variante = carrito_producto.variante

    # Devolver al stock las unidades reservadas
    if variante:
        # Devolver la cantidad del producto al stock disponible
        variante.stockProducto += carrito_producto.cantidad

        variante.save(
            update_fields=["stockProducto"]
        )


    carrito_producto.estado = False

    carrito_producto.save(
        update_fields=["estado"]
    )

    actualizar_carrito(carrito_producto.carrito)

    return redirect(
        f"/productos/{carrito_producto.producto.idProducto}/?carrito=abierto"
    )


