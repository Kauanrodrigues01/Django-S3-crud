from django.contrib import admin
from apps.galeria.models import Imagem

# Register your models here.
class ListandoImagens(admin.ModelAdmin):
    list_display = ('id', 'nome', 'categoria', 'legenda', 'user' ,'descricao', 'publicada') # Campos a serem exibidos
    list_display_links = ('id', 'nome') # Links para editar
    search_fields = ('nome',) # Campo de busca
    list_filter = ('categoria', 'user') # Filtro
    list_editable = ('publicada', 'user') # Editar na lista
    list_per_page = 15  # Paginação
    
admin.site.register(Imagem, ListandoImagens) # Registra o model no admin