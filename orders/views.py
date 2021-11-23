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
        cliente = get_object_or_404(Cliente.objects.select_related('mesa'), mesa = numero_mesa, session_key = session)
        
    else:
        return HttpResponseNotFound("Su sesion ha expirado") 
    return render(request, 'orders/menus.html', context)


# ajax request
def sugerencia(request):
    if request.method == "POST":
        pass
    return HttpResponseNotFound("No hemos encontrado nada :(")