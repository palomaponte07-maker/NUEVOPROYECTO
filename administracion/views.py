from django.shortcuts import render, redirect
from .forms import ProductoForm
from productos.models import Producto, Imagen

def dashboard(request):
    productos = Producto.objects.all().order_by('-idProducto')[:10]
    return render(
        request, 
        'administracion/dashboard.html',
        {'productos': productos} )

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            producto =form.save(commit=False)
            producto.precioDescuento = producto.precioOriginal
            producto.porcentajeDescuento = 0
            producto.save()
            return redirect('dashboard')

    else:
        form = ProductoForm()

    return render(
        request,
        'administracion/productos/agregar.html',
        {'form': form}
    )

def editar_producto(request):
    return render(request, 'administracion/productos/editar.html')
