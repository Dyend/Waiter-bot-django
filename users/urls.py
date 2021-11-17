from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', view=views.LoginView.as_view(), name = 'login'),

]