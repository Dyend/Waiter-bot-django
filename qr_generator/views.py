from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import QRForm
from orders.models import Mesa
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
                mesa.ocupada = True
                mesa.save()
                factory = qrcode.image.svg.SvgImage
                url = request.build_absolute_uri(reverse('orders:lista_menus'))
                img = qrcode.make(url, image_factory=factory, box_size=20)
                stream = BytesIO()
                img.save(stream)
                context["svg"] = stream.getvalue().decode()
            else:
                # retornar que no se encontro una mesa disponible
                pass
    else:
       context['mesas'] = Mesa.objects.all()

    return render(request, 'qr_generator/qr.html', context)