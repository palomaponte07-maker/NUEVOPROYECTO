from decimal import Decimal
from django.db import transaction 
from django.core.exceptions import ValidationError
from .models import Pedido, DetallePedido
from productos.models import Clienete
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
    metodod_pago=None
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
        "Confirmado",
        "Enviado",
        "Cancelado"
    ]
    
    

