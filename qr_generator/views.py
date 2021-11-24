from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, datetime
from .forms import QRForm
import jwt
from orders.models import Mesa, Cliente
from django.http import HttpResponseNotFound
from django.db import transaction
from waiter_bot.settings import SECRET_KEY
import qrcode
import qrcode.image.svg
from io import BytesIO

# Create your views here.

@login_required
def qr_generator(request):
    context = {}
    context['form'] = QRForm()
    
    if request.method == "POST":
        form = QRForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad_personas']
            mesa = Mesa.objects.filter(capacidad__gte=cantidad, ocupada=False).order_by('capacidad').first()
            if mesa:
                factory = qrcode.image.svg.SvgImage
                token = jwt.encode({"exp": datetime.now(timezone.utc) + timedelta(minutes=5), "numero_mesa": mesa.numero}, SECRET_KEY, algorithm="HS256")
                url = request.build_absolute_uri(reverse('qr_generator:reservar_mesa', kwargs={'token':token}))
                img = qrcode.make(url, image_factory=factory, box_size=10)
                stream = BytesIO()
                img.save(stream)
                context["svg"] = stream.getvalue().decode()
                context['mesa'] = mesa.numero
                return render(request, 'qr_generator/qr_generado.html', context)
            else:
                # retornar que no se encontro una mesa disponible
                pass
    else:
       context['mesas'] = Mesa.objects.all()

    return render(request, 'qr_generator/qr.html', context)

@transaction.atomic
def reservar_mesa(request, token):
    try:
        token = jwt.decode(token, SECRET_KEY, options={"require_exp": True}, algorithms="HS256")
    except:
        return HttpResponseNotFound("El codigo QR ha expirado :(")
    numero_mesa = token['numero_mesa']
    mesa = Mesa.objects.get(numero=numero_mesa)
    session = request.session.session_key
    if not session:
        request.session.create()
        session = request.session.session_key
    Cliente.objects.update_or_create(mesa=mesa, session_key=session)
    mesa.ocupada = True
    mesa.save()

    # Redireccionar a la mesa
    return redirect('orders:lista_menus', numero_mesa=mesa.numero)