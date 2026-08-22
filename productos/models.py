from django.db import models

class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreCategoria
    
class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE,db_column='idCategoria')

    nombre = models.CharField(max_length=100)
    precioCosto = models.DecimalField(max_digits=10,decimal_places=2)
    precioVenta = models.DecimalField(max_digits=10, decimal_places=2)
    IVA = models.DecimalField(max_digits=5, decimal_places=2, default=21)
    color = models.CharField(max_length=50)
    talle = models.CharField(max_length=20)
    descripcion = models.TextField()
    porcentajeDescuento = models.DecimalField(max_digits=10, decimal_places=2)
    fechaInicioDescuento = models.DateTimeField(null=True,blank=True)
    fechaFinDescuento = models.DateTimeField(null=True,blank=True)
    stockProducto = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)
    stockDeposito = models.IntegerField()

    def __str__(self):
        return self.nombre

class Imagen(models.Model):
    idImagen = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE,db_column='idProducto')
    urlImagen = models.CharField(max_length=255)

    def __str__(self):
        return self.urlImagen

