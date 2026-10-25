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
    def clean(self):
            cleaned_data = super().clean()

            fecha_inicio = cleaned_data.get('fechaInicioDescuento')
            fecha_fin = cleaned_data.get('fechaFinDescuento')

            if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
                self.add_error(
                    'fechaFinDescuento',
                    'La fecha de fin no puede ser anterior '
                    'a la fecha de inicio del descuento.'
                )

            return cleaned_data