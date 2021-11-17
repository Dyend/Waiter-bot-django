from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('generator/', view=views.qr_generator, name = 'qr_generator'),

]