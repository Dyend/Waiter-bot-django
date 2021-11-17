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
    objects = models.Manager()

class Mesa(models.Model):
    numero = models.IntegerField(default=0, unique=True)
    capacidad = models.IntegerField(default=1)
    ocupada = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.numero)

    objects = models.Manager()
