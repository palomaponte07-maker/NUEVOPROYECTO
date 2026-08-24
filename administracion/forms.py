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
        widgets = {
            'fechaInicioDescuento': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'fechaFinDescuento': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }
#precio venta no locolacamos xq el precio se clacula automaticamente con precio costo +IVA