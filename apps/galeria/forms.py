from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.galeria.models import Imagem

class ImagemForms(forms.ModelForm):
    class Meta:
        model = Imagem
        exclude = ['publicada']  # Exclua o campo 'user' aqui também
        fields = ['nome', 'legenda', 'categoria', 'descricao', 'caminho_imagem', 'data_imagem']  # Não inclua 'user'
        
        labels = {
            'nome': 'Nome',
            'legenda': 'Legenda',
            'categoria': 'Categoria',
            'descricao': 'Descrição',
            'caminho_imagem': 'Caminho',
            'data_imagem': 'Data',
        }
        
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control mt',
                'placeholder': 'Nome da imagem'
            }),
            'legenda': forms.TextInput(attrs={
                'class': 'form-control mt',
                'placeholder': 'Legenda da imagem'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control mt',
                'placeholder': 'Categoria da imagem'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control mt',
                'placeholder': 'Descrição da imagem',
                'rows': 5,
                'cols': 20
            }),
            'caminho_imagem': forms.FileInput(attrs={
                'class': 'form-control mt',
                'placeholder': 'Caminho da imagem',
            }),
            'data_imagem': forms.DateInput(
                format='%d/%m/%Y',  # Corrija o formato da data
                attrs={
                    'class': 'form-control mt',
                    'placeholder': 'Data da imagem',
                    'type': 'date',
                }),
        }
        
    def __init__(self, *args, **kwargs): # Adicione o argumento 'user' ao método __init__, para que ele possa ser passado ao formulário
        self.user = kwargs.pop('user', None) # Pega o valor de 'user' e o remove do dicionário kwargs
        super().__init__(*args, **kwargs) # Chama o método __init__ da classe pai, passando os argumentos recebidos

    def save(self, commit=True): # Essa função é chamada quando o formulário é salvo, e ela deve ser modificada para salvar o usuário
        instance = super().save(commit=False) # Faz uma copia do formulario sem salvar no banco de dados
        if self.user: # Se o usuário estiver definido, salve-o no campo 'user' do modelo
            instance.user = self.user # Salva o usuário no campo 'user' do modelo
        if commit: # Se commit for verdadeiro, salve o formulário no banco de dados
            instance.save() # Salva o formulário no banco de dados
        return instance