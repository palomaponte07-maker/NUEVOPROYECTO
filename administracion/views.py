from django.shortcuts import render, redirect
from .forms import ProductoForm
from productos.models import Producto, Imagen
from pedidos.models import Pedido,DetallePedido

def dashboard(request):
    productos = Producto.objects.all().order_by('-idProducto')[:10]
    for producto in productos:
        producto.precio_mostrar = f"{producto.precioVenta:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    pedidos = Pedido.objects.select_related('cliente').prefetch_related('detallepedido_set__producto').order_by('-idPedido')[:10]
    return render(
        request, 
        'administracion/dashboard.html',
        {
            'productos': productos,
            'pedidos': pedidos,

        }
    )

def agregar_producto(request):
    if request.method == 'POST':

        form = ProductoForm(request.POST,request.FILES)
        print("ARCHIVOS RECIBIDOS:", request.FILES)
        if form.is_valid():
            producto =form.save(commit=False)
            producto.porcentajeDescuento = 0
            producto.precioVenta = (
                producto.precioCosto +
                (producto.precioCosto * producto.IVA / 100)
            )
            producto.save()
            # Obtener las fotos enviadas desde el formulario
            fotos = request.FILES.getlist('foto')

            print("FOTOS:", fotos)

            # Guardar cada foto relacionada con el producto
            for foto in fotos:
                Imagen.objects.create(
                    producto=producto,
                    imagen=foto
                )

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
