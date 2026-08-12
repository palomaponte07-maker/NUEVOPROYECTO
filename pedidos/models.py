from django.db import models

class Pedido(models.Model):
    idPedido =models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE,
        db_column="idCliente"
    )

    administrador = models.ForeignKey(
        "administracion.Administrador",
        on_delete=models.CASCADE,
        db_column="idAdministrador"
    )

    numeroPedido = models.CharField(max_length=20)   
    fecha = models.DateField()
    estado = models.CharField(max_length=20)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Pedido {self.numeroPedido}"

class DetallePedido(models.Model):
    idDetallePedido = models.AutoField(primary_key=True)
 
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column="idPedido"
    )

    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        db_column="idProducto"
    )

    cantidad = models.IntegerField()

    precioUnitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subTotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Detalle {self.idDetallePedido}"

