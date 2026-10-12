from urllib import request

from django.contrib.messages.api import get_messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm
from productos.models import Producto, ProductoVariante, Imagen
from pedidos.models import Pedido,DetallePedido
from .models import Notificacion
from productos.models import Producto

from django.contrib import messages
from productos.models import Producto, Categoria, ProductoVariante

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.contrib.messages import get_messages

def dashboard(request):
    productos = Producto.objects.all().order_by('-idProducto')[:10]

    for producto in productos:
        producto.precio_mostrar = f"{producto.precioVenta:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    pedidos = Pedido.objects.select_related('cliente').prefetch_related('detallepedido_set__producto').order_by('-idPedido')[:10]

    notificaciones = Notificacion.objects.select_related(
        'pedido',
        'producto'
    ).order_by('-idNotificacion')[:5]  
    return render(
        request, 
        'administracion/dashboard.html',
        {
            'productos': productos,
            'pedidos': pedidos,
            'notificaciones': notificaciones,

        }
    )

def notificaciones(request):

    # Variantes que actualmente tienen stock 0
    variantes_sin_stock = (
        ProductoVariante.objects
        .select_related('producto')
        .filter(stockProducto=0)
        .order_by('producto__nombre')
    )

    # Últimos 5 pedidos registrados
    pedidos_recientes = (
        Pedido.objects
        .select_related('cliente')
        .order_by('-idPedido')[:5]
    )

    return render(
        request,
        'administracion/notificaciones.html',
        {
            'variantes_sin_stock': variantes_sin_stock,
            'pedidos_recientes': pedidos_recientes,
        }
    )


def detalle_pedido(request, id):
    pedido = get_object_or_404(
        Pedido.objects.select_related('cliente'),
        idPedido=id
    )

    detalles = DetallePedido.objects.filter(
        pedido=pedido
    ).select_related(
        'producto',
        'variante'
    )

    return render(
        request,
        'administracion/pedidos.html',
        {
            'pedido': pedido,
            'detalles': detalles,
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

            fotos = request.FILES.getlist('foto')
            print("FOTOS:", fotos)
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



def editar_producto(request, idProducto):
    producto = get_object_or_404(
        Producto.objects.prefetch_related(
            'variantes',
            'imagen_set'
        ),
        idProducto=idProducto
    )

    variantes = list(producto.variantes.all())
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        try:
            # 1. Validar que la categoría exista
            categoria_id = request.POST.get('categoria')

            categoria = Categoria.objects.filter(
                idCategoria=categoria_id
            ).first()

            if categoria is None:
                raise ValueError('La categoría seleccionada no existe.')

            # 2. Cargar los datos generales
            producto.nombre = request.POST.get('nombre', '').strip()
            producto.categoria = categoria

            
            producto.precioCosto = Decimal(request.POST.get('precioCosto', ''))
            producto.IVA = Decimal(request.POST.get('IVA', ''))

            # Calcular automáticamente el precio de venta
           
            producto.precioVenta = (
                producto.precioCosto
                + (producto.precioCosto * producto.IVA / Decimal('100'))
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            producto.full_clean()

            producto.porcentajeDescuento = Decimal(
                request.POST.get('porcentajeDescuento', '')
            )
            producto.descripcion = request.POST.get(
                'descripcion', ''
            ).strip()

            # 3. Convertir las fechas del formulario
            fecha_inicio = request.POST.get(
                'fechaInicioDescuento', ''
            ).strip()
            fecha_fin = request.POST.get(
                'fechaFinDescuento', ''
            ).strip()

            producto.fechaInicioDescuento = (
                datetime.strptime(
                    fecha_inicio, '%Y-%m-%dT%H:%M'
                ) if fecha_inicio else None
            )

            producto.fechaFinDescuento = (
                datetime.strptime(
                    fecha_fin, '%Y-%m-%dT%H:%M'
                ) if fecha_fin else None
            )

            if settings.USE_TZ:
                if producto.fechaInicioDescuento:
                    producto.fechaInicioDescuento = timezone.make_aware(
                        producto.fechaInicioDescuento,
                        timezone.get_current_timezone()
                    )

                if producto.fechaFinDescuento:
                    producto.fechaFinDescuento = timezone.make_aware(
                        producto.fechaFinDescuento,
                        timezone.get_current_timezone()
                    )

            # 4. Comprobar que el período del descuento sea coherente
            if (
                producto.fechaInicioDescuento
                and producto.fechaFinDescuento
                and producto.fechaFinDescuento
                < producto.fechaInicioDescuento
            ):
                raise ValueError(
                    'La fecha de fin no puede ser anterior '
                    'a la fecha de inicio del descuento.'
                )

            # 5. Validar el producto sin guardarlo todavía
            producto.full_clean()

            # 6. Preparar y validar todas las variantes existentes
            for variante in variantes:
                variante.color = request.POST.get(
                    f'color_{variante.idVariante}', ''
                ).strip()

                variante.talle = request.POST.get(
                    f'talle_{variante.idVariante}', ''
                ).strip()

                variante.stockProducto = int(
                    request.POST.get(
                        f'stockProducto_{variante.idVariante}', ''
                    )
                )

                variante.stockDeposito = int(
                    request.POST.get(
                        f'stockDeposito_{variante.idVariante}', ''
                    )
                )

                variante.full_clean()

            # 7. Guardar todo dentro de una única transacción
            with transaction.atomic():
                producto.save()

                for variante in variantes:
                    variante.save()

            # Limpiar mensajes anteriores pendientes
            list(get_messages(request))           
            messages.success(
                request,
                'Producto actualizado correctamente.'
            )
            return redirect('editar_producto', idProducto=producto.idProducto)

            return redirect(
                'editar_producto',
                idProducto=producto.idProducto
            )

        except (
            ValidationError,
            ValueError,
            TypeError,
            InvalidOperation
        ) as error:
            messages.error(
                request,
                f'No se pudieron guardar los cambios: {error}'
            )

    return render(
        request,
        'administracion/productos/editar.html',
        {
            'producto': producto,
            'variantes': variantes,
            'categorias': categorias,
        }
    )



def cambiar_estado_producto(request, id):
    producto = get_object_or_404(
        Producto,
        idProducto=id
    )

    if request.method == 'POST':
        producto.estado = not producto.estado
        producto.save()

    return redirect('dashboard')

