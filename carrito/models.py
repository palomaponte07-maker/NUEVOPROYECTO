from django.db import models

class Carrito(models.Model):
    idCarrito = models.AutoField(primary_key=True)
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE, db_column="idCliente")

    fechaCreacion = models.DateTimeField()
    fechaExpiracion = models.DateTimeField(blank=True, null=True)
    numeroPedido = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estadoPago = models.CharField(max_length=20, blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    precioUnitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subTotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    class Meta:
        db_table = 'Carrito'
    def __str__(self):
        return f"Carrito {self.idCarrito}" 

class CarritoProducto(models.Model):
    idCarritoProducto = models.AutoField(primary_key=True)

    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        db_column="idCarrito",
    )

    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        db_column="idProducto"
    )

    variante = models.ForeignKey(
        "productos.ProductoVariante",
        on_delete=models.CASCADE,
        db_column="idVariante",
        null=True,
        blank=True
    )

    numeroPedido = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estadoPago = models.CharField(max_length=20, blank=True, null=True)
    cantidad = models.IntegerField()
    precioUnitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    subTotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'CarritoProducto'

    def __str__(self):
        return f"CarritoProducto {self.carrito.idCarrito} - {self.producto.nombre}"