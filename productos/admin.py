from django.contrib import admin
from .models import Categoria, Producto, Imagen, ProductoVariante

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(ProductoVariante)
admin.site.register(Imagen)


# Register your models here.
