from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('<int:numero_mesa>', views.lista_menus, name='lista_menus'),
    path('sugerencia/', views.lista_menus, name='sugerencia'),
]