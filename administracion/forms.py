from django import forms
from productos.models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'categoria',
            'nombre',
            'descripcion',
            'precioOriginal',
            'color',
            'talle',
            'stock',
        ]
