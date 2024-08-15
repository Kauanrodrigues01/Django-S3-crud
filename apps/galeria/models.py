from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Imagem(models.Model):
    OPCOES_CATEGORIA = [
        ('NEBULOSA', 'Nebulosa'),
        ('GALÁXIA', 'Galáxia'),
        ('PLANETA', 'Planeta'),
        ('ESTRELA', 'Estrela'),
        ('OUTRO', 'Outro'),
    ]
    
    nome = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=200, null=False, blank=False)
    categoria = models.CharField(max_length=30,choices=OPCOES_CATEGORIA, default='')
    descricao = models.TextField(null=False, blank=False)
    caminho_imagem = models.ImageField(upload_to='fotos/%Y/%m/%d/', blank=True)
    publicada = models.BooleanField(default=True)
    data_imagem = models.DateField(null=False, blank=False, default=datetime.datetime.now)
    user = models.ForeignKey(
        to=User, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=False,
        related_name='user',
    )

    def __str__(self):
        return self.nome