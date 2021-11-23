from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from .models import *

# Create your views here.

def lista_menus(request, numero_mesa):
    context = {}
    session = request.session.session_key
    if session:
        # Se verifica que esta sesion pertenezca a la mesa
        cliente = get_object_or_404(Cliente, mesa = numero_mesa, session_key = session)
        pedidos = Pedido.objects.filter(mesa = numero_mesa).select_related('plato')
        menus = Menu.objects.all()
        context['pedidos'] = pedidos
        context['menus'] = menus
    else:
        return HttpResponseNotFound("Su sesion ha expirado") 
    return render(request, 'orders/menus.html', context)


# ajax request
def sugerencia(request, ):
    if request.method == "POST":
        pass
    return HttpResponseNotFound("No hemos encontrado nada :(")

# ajax request
def agregar_pedido(request, numero_mesa, id_plato):
    context = {}
    session = request.session.session_key
    if session:
        # Se verifica que esta sesion pertenezca a la mesa
        cliente = get_object_or_404(Cliente, mesa = numero_mesa, session_key = session)
        plato = get_object_or_404(Menu, id=id_plato)
        pedido = Pedido.objects.create(plato=plato, mesa = numero_mesa)
        context['pedido'] = pedido
        return render(request, 'orders/plato.html', context)
    return HttpResponseNotFound("No hemos encontrado nada :(")

