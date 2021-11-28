import admin_thumbnails
from django.contrib import admin
from .models import *
# Register your models here.


class IngredientesInline(admin.TabularInline):
    model = Ingrediente.menus.through

@admin_thumbnails.thumbnail('imagen')
class MenuAdmin(admin.ModelAdmin):
    inlines = [IngredientesInline, ]



admin.site.register(Mesa)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Cliente)
admin.site.register(Ingrediente)
admin.site.register(Pedido)