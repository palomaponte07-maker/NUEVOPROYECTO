from django.db import models

class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length = 100)
    apellido = models.CharField(max_length = 100)
    DNI = models.CharField(max_length = 15)
    telefono = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 150)
    calle = models.CharField(max_length = 150)
    numCalle = models.CharField(max_length = 10)
    codPostal = models.CharField(max_length = 10)
    ciudad = models.CharField(max_length = 100)
    provincia = models.CharField(max_length = 100)

    class Meta:
        db_table = 'Cliente'
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

