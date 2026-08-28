from django.shortcuts import render

def carrito(request):
    return render(request, 'cliente/carrito_producto.html')