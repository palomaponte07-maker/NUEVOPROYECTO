from django.urls import path 
from .views import dashboard 
from .views import dashboard, agregar_producto
from . import views

urlpatterns = [ 
    path('', dashboard, name='dashboard'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('productos/agregar/', agregar_producto, name='agregar_producto'),    
    path('productos/editar/<int:idProducto>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:idProducto>/',views.eliminar_producto,name='eliminar_producto'),
    path('producto/<int:id>/cambiar-estado/', views.cambiar_estado_producto, name='cambiar_estado_producto'),
    path('pedido/<int:id>/', views.detalle_pedido, name='detalle_pedido'),
    
path(
    'productos/',
    views.todos_los_productos,
    name='todos_los_productos'
),

path(
    'pedidos/',
    views.todos_los_pedidos,
    name='todos_los_pedidos'
),
]
