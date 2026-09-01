from decimal import Decimal
from django.conf.locale import de
from django.db import transaction 
from django.core.exceptions import ValidationError
from .models import Pedido, DetallePedido
from productos.models import Clienete, Producto, ProductoVariante
from administracion.models import Administrador
from clientes.models import Cliente


def calcular_total_pedido(pedido):
    """ recalcular la cintidad de total y el total monetario del pedido a partir de sus detalles."""
    detalles = DetallePedido.objects.filter(pedido=pedido)
    cantidad_total = 0
    total = Decimal("0.00")
    for detalle in detalles:
        cantidad_total+= detalle.cantidad
        total += detalle.subTotal

    pedido.cantidad = cantidad_total
    pedido.total = total
    pedido.save(update_fields=["cantidad", "total"])
    return pedido

@transaction.automic
def crear_pedido(
    cliente_id,
    administracion_id,
    numero_pedido,
    fecha,
    estado_pago="pendiente",
    cod_transaccion=None,
    fecha_pago=None,
    metodo_pago=None
):
    """ Crea un pedido nuevo """
    
    cliente = Cliente.objects.get(pk=cliente_id)
    administrador = Administrador.objects.get(pk=administrador_id)

    if not numero_pedido:
        raise ValidationError(
            "El número de pedido es obligatorio."
        )

    estados_validos =[
        "Pendiente",
        "Pagado",
        "Cancelado"
    ]

    if estado_pago not in estados_validos:
        raise ValidationError(
            "el estado del pago no es válido"
        )
    
    if estado_pago == "Pagado":
        raise ValidationError(
            "Un pedido pagado debe tener un método de pago."
        )
    if not cod_transaccion:
        raise ValidationError(
            "Un pedido pagado debe tener código de transacción."
        )
    pedido = Pedido.objects.create(
        cliente = cliente,
        administrador = administrador,
        numeroPedido = numero_pedido,
        fecha = fecha,
        total = Decimal("0.00"),
        estadoPago = estado_pago,
        cantidad=0,
        codTransaccion = cod_transaccion,
        fechaPago = fecha_pago,
        metodoPago = metodo_pago
    )
    return pedido
@transaction.atomic
def agregar_detalle(
    pedido_id,
    producto_id,
    cantidad,
    variante_id=None
):
    """ Agregar un prducto al pedido.
    Validar producto, variante, cantidad, y stock."""

    pedido = Pedido.objects.get(pk=pedido_id)
    producto = Producto.objects.get(pk=producto_id)
    if cantidad <= 0:
        raise ValidationError(
            "La cantidad debe ser mayor a cero."
        )
    variante =None
    if variante_id is not None:
        variante = ProductoVariante.objects.get(
            pk=variante_id
        )
    if variante.producto_id ! = producto.idProducto:
        raise ValidationError(
            "la variante no pertenece al producto seleccionado."
        )
    if cantidad > variante.stockProducto:
        raise ValidationError(
            "No hay suficiente stock disponible"
        )
    precio_unitario = producto.precioVenta 
    else:
    precio_unitario = producto.precioVenta
    subtotal = Decimal(cantidad) * precio_unitario
    detalle = DetallePedido.objects.create(
        pedido=pedido,
        producto=producto,
        variante=variante,
        cantidad=cantidad,
        precioUnitario=precio_unitario,
        subTotal=subtotal
    )
    if variante is not None:
        variante.stockProducto -= cantidad
        variante.save(update_fields=["stockProducto"])

    calcular_total_pedido(pedido)
    return detalle
@transaction.atomic
def actualizar_detall(
    detalle_id,
    nueva_cantidad
):
    """ Actualiza la cantidad de un detalle
    Ajusta el stock y recalcula el subtotal y el pedido."""
    detalle = DetallePedido.objects.select_for_update().get(
        pk=detalle_id
    )
    if nueva_cantidad <= 0:
        raise ValidationError(
            "La cantidad debe ser mayor a cero."
        )
    ccantidad_anterior = detalle.cantidad
    diferencia = nueva_cantidad - ccantidad_anterior

    if detalle.variante:
        variante = ProductoVariante.objects.select_for_update().get(
            pk=detalle.variante_id
        )
        if diferencia > 0:
            if diferencia > variante.stockProducto:
                raise ValidationError(
                    "No hay suficiente stock para aumentar la cantidad"
                )
            variante.stockProducto -=diferencia
        elif diferencia < 0:
            variante.stockProducto += abs(diferencia)
        variante.save(
            update_fields=["stockProducto"]
        )
        detalle.subTotal = (
            Decimal(nueva_cantidad) * detalle.precioUnitario 
        )
        detalle.save(
            update_fields=["cantidad", "subTotal"]
        )
        calcular_total_pedido(detalle.pedido)
        return detalle
@transaction.atomic
def eliminar_detalle(detalle_id):
    """Eliminar un detalle y devuelva el stock correspondiente."""
    detalle = DetallePedido.objects.select_for_update().get(
        pk=detalle_id
    )

    pedido = detalle.pedido
    if detalle.variante:
        variante.stockProducto += detalle.cantidad
        variante.save(
            update_fields=["stockProducto"]
        )
    detalle.delete()
    calcular_total_pedido(pedido)
    return pedido
@transaction.atomic
def eliminar_pedido(pedido_id):
    """Eliminar un pedido completo.
    Devuelve al stock las cantidades de sus variante"""
    pedido = Pedido.objects.select_for_update().get(
        pk=pedido_id
    )
    detalles = DetallePedido.objects.filter(
       "variante" 
    ).filter(pedido=pedido)
    for detalle in detalles:
        if detalle.variante:
            variante = ProductoVariante.objects.select_for_update().get(
                pk=detalle.variante_id
            )
            variante.stockProducto += detalle.cantidad
            variante.save(
                update_fields=["stockProducto"]
            )
    pedido.delete()
    return True
