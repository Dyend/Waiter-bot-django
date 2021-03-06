import json
from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from .bot import pairs, reflections
from nltk.chat.util import Chat
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import *

# Create your views here.

chat = Chat(pairs, reflections)


def lista_menus(request, numero_mesa):
    context = {}
    session = request.session.session_key
    if session:
        # Se verifica que esta sesion pertenezca a la mesa
        cliente = get_object_or_404(
            Cliente.objects.select_related("mesa"), mesa=numero_mesa, session_key=session)
        pedidos = Pedido.objects.filter(
            mesa=numero_mesa).select_related('plato')
        menus = Menu.objects.all()
        context['pedidos'] = pedidos
        context['menus'] = menus
        context['mesa'] = numero_mesa
        context['total'] = get_total_pedido(request, numero_mesa, cliente, pedidos)
    else:
        return HttpResponseNotFound("Su sesion ha expirado")
    return render(request, 'orders/menus.html', context)


# ajax request
def sugerencia(request, id_mesa):
    if request.method == "POST":
        text_to_bot = request.POST.get('text_to_bot').lower()
        context = {
            'respuesta': chat.respond(text_to_bot)
        }
        # TODO falta fixear cuando no encuentra un plato
        if "ingredientes" in text_to_bot:
            context['tipo'] = "mensaje-recomendacion"
            ingredientes = text_to_bot.split("ingredientes ")[1].split(",")
            plato = Menu.objects.filter(ingrediente__nombre__in=ingredientes).distinct()[0]
            # Pequeño hack para no tener que serializar 
            context['menu'] = model_to_dict(plato, exclude=['precio', 'imagen', 'id'])
            context['menu']['imagen'] = plato.imagen.url
            context['menu']['precio'] = plato.precio.amount
            context['menu']['ingredientes'] = [p.nombre for p in plato.ingrediente_set.all()]
            context['menu']['url'] = (reverse('orders:agregar_pedido', kwargs={'id_plato':plato.id, 'numero_mesa': id_mesa})) #reverse con el id del plato
        else: 
            context['tipo'] = "mensaje-bot"

        return JsonResponse(context)
    return HttpResponseNotFound("No hemos encontrado nada :(")

# ajax request


def agregar_pedido(request, numero_mesa, id_plato):
    context = {}
    session = request.session.session_key
    if session:
        # Se verifica que esta sesion pertenezca a la mesa
        cliente = get_object_or_404(
            Cliente, mesa=numero_mesa, session_key=session)
        menu = get_object_or_404(Menu, id=id_plato)
        Pedido.objects.create(plato=menu, mesa_id=numero_mesa)
        context['total'] =  get_total_pedido(request, numero_mesa)
        partial_context = {'menu': menu}
        context["html"] = render_to_string('orders/plato.html', context=partial_context, request=request)
        return JsonResponse(context)
    return HttpResponseNotFound("No hemos encontrado nada :(")

def get_total_pedido(request, numero_mesa, cliente=None, pedidos=None):
    if not cliente:
        cliente = get_object_or_404(Cliente.objects.select_related("mesa"), session_key=request.session.session_key, mesa=numero_mesa)
    total = cliente.mesa.total(pedidos)
    return total

def portal_pago(request, numero_mesa):
    cliente = get_object_or_404(Cliente.objects.select_related("mesa"), session_key=request.session.session_key, mesa=numero_mesa)
    if request.method == 'GET':
        total = get_total_pedido(request, numero_mesa, cliente)
        return render(request, 'orders/pago.html', {'total': Money(amount=total, currency='CLP', decimal_places=0)})
    else:
        mesa = cliente.mesa
        Pedido.objects.filter(mesa=mesa).delete()
        Cliente.objects.filter(mesa=mesa).delete()
        mesa.ocupada = False
        mesa.save()
        return render(request, 'orders/finalizado.html')