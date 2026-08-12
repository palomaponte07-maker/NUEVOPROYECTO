from django.db import models

class MetodoPago(models.Model):
    idMetodoPago = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Pago(models.Model):
    idPago = models.AutoField(primary_key=True)

    pedido = models.ForeignKey(
        "pedidos.Pedido",
        on_delete=models.CASCADE,
        db_column="idPedido"
    )

    metodoPago = models.ForeignKey(
        MetodoPago,
        on_delete=models.CASCADE,
        db_column="idMetodoPago"
    )

    estadoPago = models.CharField(max_length=20)
    codTransaccion = models.CharField(max_length=100)
    fechaPago = models.DateField()

    def __str__(self):
        return f"Pago {self.idPago}"