from django.db import models

class Carrito(models.Model):
    idCarrito = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.CASCADE,
        db_column="idCliente",
        null=True,
        blank=True
    )

    fechaCreacion = models.DateField()

    def __str__(self):
        return f"Carrito {self.idCarrito}" 

class CarritoProducto(models.Model):
    idCarritoProducto = models.AutoField(primary_key=True)

    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        db_column="idCarrito"
    )

    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        db_column="idProducto"
    )

    cantidad = models.IntegerField()

    def __str__(self):
        return f"CarritoProducto {self.carrito.idCarrito} - {self.producto.nombre}"
    