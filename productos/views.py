from django.shortcuts import render

def inicio(request):
    return render(request, "cliente/inicio.html")

def productos(request):
    return render(request, "cliente/productos.html")

