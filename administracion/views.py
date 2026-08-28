from django.shortcuts import render, redirect,get_object_or_404
from .forms import ProductoForm
from productos.models import Producto, ProductoVariante, Imagen
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
            producto.precioVenta = (
                producto.precioCosto +
                (producto.precioCosto * producto.IVA / 100)
            )
            producto.save()
            colores = request.POST.getlist('color[]') 
            talles = request.POST.getlist('talle[]') 
            stocks_producto = request.POST.getlist('stockProducto[]') 
            stocks_deposito = request.POST.getlist('stockDeposito[]') 
            for color, talle, stock_producto, stock_deposito in zip( 
                colores, 
                talles, 
                stocks_producto, 
                stocks_deposito ): 
                    ProductoVariante.objects.create( 
                        producto=producto, 
                        color=color, talle=talle, 
                        stockProducto=int(stock_producto or 0), 
                        stockDeposito=int(stock_deposito or 0) )

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

def cambiar_estado_producto(request, id):
    producto = get_object_or_404(
        Producto,
        idProducto=id
    )

    if request.method == 'POST':
        producto.estado = not producto.estado
        producto.save()

    return redirect('dashboard')

