from django.urls import path
from apps.usuarios.views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('logout/', logout, name='logout'),
    path('perfil/', perfil, name='perfil')
]