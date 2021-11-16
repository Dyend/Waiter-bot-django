from django.shortcuts import render

# Create your views here.

def lista_menus(request):
    context = {}
    return render(request, 'orders/menus.html', context)