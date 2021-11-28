from enum import unique
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from djmoney.models.validators import MinMoneyValidator
# Create your models here.

class Menu(models.Model):
    
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    precio = MoneyField(
        max_digits=14,
        decimal_places=0,
        default_currency='CLP',
        validators=[
            MinMoneyValidator(10),
        ]
    )
    imagen = models.ImageField(null=True, blank=True)
    objects = models.Manager()
    def __str__(self) -> str:
        return self.nombre

class Ingrediente(models.Model):

    nombre = models.CharField(max_length=50, unique=True)
    menus = models.ManyToManyField('orders.Menu')
    def __str__(self) -> str:
        return self.nombre

class Mesa(models.Model):
    numero = models.IntegerField(default=0, unique=True)
    capacidad = models.IntegerField(default=1)
    ocupada = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.numero)

    def total(self, pedidos=None):
        if pedidos == None:
            pedidos = Pedido.objects.filter(mesa=self.id).select_related('plato')
        total = 0
        for pedido in pedidos:
            total = pedido.plato.precio.amount + total
        return total 

    objects = models.Manager()

# Representa un cliente de una mesa
class Cliente(models.Model):
    mesa = models.ForeignKey('orders.Mesa', on_delete = models.CASCADE)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    objects = models.Manager()

# representa un pedido de una mesa
class Pedido(models.Model):
    plato = models.ForeignKey('orders.Menu', on_delete=models.CASCADE)
    mesa = models.ForeignKey('orders.Mesa', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    objects = models.Manager()