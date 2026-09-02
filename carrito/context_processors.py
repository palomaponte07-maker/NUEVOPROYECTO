from decimal import Decimal
from .models import Carrito, CarritoProducto


def carrito_context(request):

    idCarrito = request.session.get("idCarrito")

    productos_carrito = []
    subtotal = Decimal("0.00")
    cantidad = 0

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
                (item.subTotal or Decimal("0.00"))
                for item in productos_carrito
            )

            cantidad = sum(
                (item.cantidad or 0)
                for item in productos_carrito
            )

    iva = subtotal * Decimal("0.21")
    total = subtotal + iva

    return {
        "productos_carrito": productos_carrito,
        "cantidad_carrito": cantidad,
        "subtotal_carrito": subtotal,
        "iva_carrito": iva,
        "total_carrito": total,
    }