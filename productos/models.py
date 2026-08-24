from django.db import models


class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreCategoria


class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        db_column='idCategoria'
    )

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    precioVenta = models.DecimalField(max_digits=10, decimal_places=2)
    precioCosto = models.DecimalField(max_digits=10, decimal_places=2)
    IVA = models.DecimalField(max_digits=5, decimal_places=2)

    color = models.CharField(max_length=50)
    talle = models.CharField(max_length=20)

    porcentajeDescuento = models.DecimalField(max_digits=10, decimal_places=2)
    fechaInicioDescuento = models.DateTimeField()
    fechaFinDescuento = models.DateTimeField()

    stockProducto = models.IntegerField()
    estado = models.BooleanField()
    stockDeposito = models.IntegerField()

    def __str__(self):
        return self.nombre


class Imagen(models.Model):
    idImagen = models.AutoField(primary_key=True)

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='idProducto'
    )

    urlImagen = models.CharField(max_length=255)

    def __str__(self):
        return self.urlImagen