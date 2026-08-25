from django import forms
from productos.models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'categoria',
            'nombre',
            'descripcion',
            'precioVenta',
            'precioCosto',
            'IVA',
            'porcentajeDescuento',
            'fechaInicioDescuento',
            'fechaFinDescuento',
            'estado',
        ]
        widgets = {
            'fechaInicioDescuento': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'fechaFinDescuento': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }
