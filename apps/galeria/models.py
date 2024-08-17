from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class Imagem(models.Model):
    OPCOES_CATEGORIA = [
        ('NEBULOSA', 'Nebulosa'), # 'NEBULOSA' é o valor que vai ser salvo no banco de dados, 'Nebulosa' é o valor que vai ser exibido no formulário
        ('GALÁXIA', 'Galáxia'), # 'GALÁXIA' é o valor que vai ser salvo no banco de dados, 'Galáxia' é o valor que vai ser exibido no formulário
        ('PLANETA', 'Planeta'), # 'PLANETA' é o valor que vai ser salvo no banco de dados, 'Planeta' é o valor que vai ser exibido no formulário
        ('ESTRELA', 'Estrela'), # 'ESTRELA' é o valor que vai ser salvo no banco de dados, 'Estrela' é o valor que vai ser exibido no formulário
        ('OUTRO', 'Outro'), # 'OUTRO' é o valor que vai ser salvo no banco de dados, 'Outro' é o valor que vai ser exibido no formulário
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
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.nome
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagem = models.ForeignKey(Imagem, on_delete=models.CASCADE, related_name='user_likes') # O related_name é o nome que será usado para acessar os likes de uma imagem, quando estivermos acessando a imagem e quisermos pegar os Likes podemos usar: imagem.user_likes.all()
    liked_at = models.DateTimeField(auto_now_add=True) # Data em que a imagem foi favoritada

    class Meta:
        unique_together = ('user', 'imagem')  # Para garantir que um usuário só possa curtir uma imagem uma vez

    def __str__(self):
        return f"{self.user.username} likes {self.image.title}"
    
class Favoritas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favoritas')
    imagem = models.ForeignKey(Imagem, on_delete=models.CASCADE, related_name='user_favoritas') # O related_name é o nome que será usado para acessar as imagens favoritas de um usuário, quando estivermos acessando o usuário e quisermos pegar as imagens favoritas podemos usar: imagem.user_favorites.all()
    favoritada = models.BooleanField(default=False)
    favoritada_at = models.DateTimeField(auto_now_add=True) # Data em que a imagem foi favoritada
    
    class Meta:
        unique_together = ('user', 'imagem')
    
    def __str__(self):
        return f"{self.user.username} favoritou {self.image.title}"