from django.shortcuts import render, redirect
from .forms import ProductoForm

def dashboard(request):
    return render(request, 'administracion/dashboard.html')

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
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
