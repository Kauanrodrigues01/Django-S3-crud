from django.urls import path
from apps.galeria.views import *

urlpatterns = [
    path('', index, name='index'),
    path('categoria/<str:categoria>/', index, name='index_com_categoria'),
    path('imagem/<int:imagem_id>', imagem, name='imagem'),
    path('buscar', buscar, name='buscar'),
    path('nova-imagem', nova_imagem, name='nova_imagem'),
    path('editar-imagem', editar_imagem, name='editar_imagem'),
    path('deletar-imagem/<int:imagem_id>', deletar_imagem, name='deletar_imagem'),
    path('favoritar-imagem/<int:imagem_id>', favoritar_imagem, name='favoritar_imagem'),
]