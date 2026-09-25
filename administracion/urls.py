from django.urls import path 
from .views import dashboard 
from .views import dashboard, agregar_producto
from . import views

urlpatterns = [ 
    path('', dashboard, name='dashboard'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('productos/agregar/', agregar_producto, name='agregar_producto'),
    path('productos/editar/', views.editar_producto, name='editar_producto'),
    path('producto/<int:id>/cambiar-estado/', views.cambiar_estado_producto, name='cambiar_estado_producto'),
    path('pedido/<int:id>/', views.detalle_pedido, name='detalle_pedido'),
]