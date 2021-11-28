from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('<int:numero_mesa>', views.lista_menus, name='lista_menus'),
    path('sugerencia/<int:id_mesa>', views.sugerencia, name='sugerencia'),
    path('agregar_pedido/<int:numero_mesa>/<int:id_plato>', views.agregar_pedido, name='agregar_pedido'),
]