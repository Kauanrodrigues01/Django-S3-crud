from django.urls import path
from apps.galeria.views import *

urlpatterns = [
    path('', index, name='index'),
    path('imagem/<int:imagem_id>', imagem, name='imagem'),
    path('buscar', buscar, name='buscar'),
    path('nova-imagem', nova_imagem, name='nova_imagem'),
    path('editar-imagem', editar_imagem, name='editar_imagem'),
    path('deletar-imagem', deletar_imagem, name='deletar_imagem')
]