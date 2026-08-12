from django.db import models

class Contacto(models.Model):
    idContacto = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=20)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
