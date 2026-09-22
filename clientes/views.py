from django.shortcuts import render, redirect
from .models import Carrito
from clientes.models import Cliente


def iniciar_compra(request):

    carrito = Carrito.objects.get_or_create(cliente=None)[0]

    if request.method == "POST":

        cliente = Cliente.objects.create(
            nombre=request.POST.get("nombre"),
            apellido=request.POST.get("apellido"),
            DNI=request.POST.get("DNI"),
            telefono=request.POST.get("telefono"),
            email=request.POST.get("email"),
            calle=request.POST.get("calle"),
            numCalle=request.POST.get("numCalle"),
            codPostal=request.POST.get("codPostal"),
            ciudad=request.POST.get("ciudad"),
            provincia=request.POST.get("provincia"),
        )

        # Asociamos el cliente al carrito
        carrito.cliente = cliente
        carrito.save()

        return redirect("...")
    
    return render(
        request,
        "cliente/carrito_producto.html",
        {
            "carrito": carrito,
        }
    )