from django.urls import path 
from .views import dashboard 
from .views import dashboard, agregar_producto

urlpatterns = [ 
    path('', dashboard, name='dashboard')
]
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('productos/agregar/', agregar_producto, name='agregar_producto'),
]