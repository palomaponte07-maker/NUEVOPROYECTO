from django import forms
from productos.models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'categoria',
            'nombre',
            'descripcion',
            'precioCosto',
            'precioVenta',
            'IVA',
            'color',
            'talle',
            'procentajeDescuento',
            'fechaInicioDescuento',
            'fechaFinDescuento',
            'stockProducto',
            'stockDeposito',
            'estado',
        ]
