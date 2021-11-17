from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import *

# Create your views here.

def lista_menus(request):
    context = {}
    return render(request, 'orders/menus.html', context)


# ajax request
def sugerencia(request):
    if request.method == "POST":
        pass
    return HttpResponseNotFound("No hemos encontrado nada :(")