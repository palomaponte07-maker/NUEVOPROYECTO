from django.db import models

class Administrador(models.Model):
    idAdministrador = models.AutoField(primary_key=True)

    nombreAdministrador = models.CharField(max_length=100)
    class Meta:
        db_table = 'Administrador'
    def __str__(self):
        return self.nombreAdministrador

class Notificacion(models.Model):
    idNotificacion = models.AutoField(primary_key=True)

    administrador = models.ForeignKey(
        Administrador,
        on_delete=models.CASCADE,
        db_column="idAdministrador"
    )

    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        db_column="idProducto"
    )

    pedido = models.ForeignKey(
        "pedidos.Pedido",
        on_delete=models.CASCADE,
        db_column="idPedido",
        null = True,
        blank = True
    )

    fecha = models.DateField()

    class Meta:
        db_table = 'Notificacion'

    def __str__(self):
        return f"Notificación {self.idNotificacion}"

