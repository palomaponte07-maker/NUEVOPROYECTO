from django.shortcuts import render

def dashboard(request):
    return render(request, 'administracion/dashboard.html')

def agregar_producto(request):
    return render(request, 'administracion/productos/agregar.html')

def editar_producto(request):
    return render(request, 'administracion/productos/editar.html')