from django.db import models


class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=50)

    class Meta:
        db_table = 'Categoria'
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
    precioCosto = models.DecimalField(max_digits=10, decimal_places=2)
    precioVenta = models.DecimalField(max_digits=10, decimal_places=2)
    IVA = models.DecimalField(max_digits=5, decimal_places=2, default=21)

    descripcion = models.TextField()

    porcentajeDescuento = models.DecimalField(max_digits=10,decimal_places=2)
    fechaInicioDescuento = models.DateTimeField(null=True,blank=True)
    fechaFinDescuento = models.DateTimeField(null=True,blank=True)

    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'Producto'
    def __str__(self):
        return self.nombre


class ProductoVariante(models.Model):
     idVariante = models.AutoField(primary_key=True)

     producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='idProducto',
        related_name='variantes'
    )

     color = models.CharField(max_length=50)
     talle = models.CharField(max_length=20)

     stockProducto = models.IntegerField(default=0)
     stockDeposito = models.IntegerField(default=0)

     class Meta:
        db_table = 'ProductoVariante'
     def __str__(self):
        return f"{self.producto.nombre} - {self.color} - {self.talle}"

class Imagen(models.Model):
    idImagen = models.AutoField(primary_key=True)

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='idProducto'
    )

    variante = models.ForeignKey(
        ProductoVariante,
        on_delete=models.CASCADE,
        db_column='idVariante',
        null=True,
        blank=True
    )

    urlImagen = models.CharField(max_length=255)
    class Meta:
        db_table = 'Imagen'
    def __str__(self):
        return self.urlImagen