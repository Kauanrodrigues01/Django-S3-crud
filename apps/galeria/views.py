from django.shortcuts import render, get_object_or_404, redirect

from apps.galeria.models import Imagem, Like, Favoritas
from apps.galeria.forms import ImagemForms

from django.contrib import messages

# Create your views here.

def index(request, categoria=None):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    if categoria:
        if categoria == 'FAVORITAS':
            # Obtenha os IDs das imagens favoritas do usuário
            imagens_favoritadas_ids = Favoritas.objects.filter(user=request.user).values_list('imagem_id', flat=True)
            # Filtre as imagens para mostrar apenas aquelas que são favoritas
            imagens = Imagem.objects.filter(id__in=imagens_favoritadas_ids) # o id__in é um filtro que retorna apenas os objetos cujo id está na lista passada
        else:
            imagens = Imagem.objects.filter(publicada=True, categoria=categoria)
    else:
        imagens = Imagem.objects.filter(publicada=True)

    likes_do_usuario = Like.objects.filter(user=request.user).values_list('imagem_id', flat=True) # values_list('image_id', flat=True) retorna uma lista de IDs de imagens curtidas pelo usuário
    imagens_favoritadas_do_usuario = Favoritas.objects.filter(user=request.user).values_list('imagem_id', flat=True) # values_list('image_id', flat=True) retorna uma lista de IDs de imagens favoritadas pelo usuário
    
    return render(request, 'galeria/index.html', {
        'cards': imagens,
        'likes_do_usuario': likes_do_usuario,
        'imagens_favoritadas_do_usuario': imagens_favoritadas_do_usuario,
    })

def imagem(request, imagem_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    imagem = get_object_or_404(Imagem, pk=imagem_id)
    
    quantidade_likes = imagem.user_likes.count() # Conta quantos likes a imagem tem
    
    imagens_favoritadas_do_usuario = Favoritas.objects.filter(user=request.user).values_list('imagem_id', flat=True) # values_list('image_id', flat=True) retorna uma lista de IDs de imagens favoritadas pelo usuário
    
    likes_do_usuario = Like.objects.filter(user=request.user).values_list('imagem_id', flat=True) # values_list('image_id', flat=True) retorna uma lista de IDs de imagens que o usuário deu like
    
    return render(request, 'galeria/imagem.html', {
        'imagem': imagem,
        'quantidade_likes': quantidade_likes,
        'imagens_favoritadas_do_usuario': imagens_favoritadas_do_usuario,
        'likes_do_usuario': likes_do_usuario
        })

def buscar(request):
    
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    todas_imagens = Imagem.objects.all().filter(publicada=True)
    
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar'] # pega o valor do campo de busca, na url
        nome_a_buscar = nome_a_buscar.strip()
        
        # Verificação se o campo de busca está vazio ou contém apenas espaços em branco
        if not nome_a_buscar:
            messages.error(request, 'Digite algo para buscar')
            return redirect('index')
        
        # Realiza a busca apenas se houver um termo válido
        imagens = todas_imagens.filter(
            nome__icontains=nome_a_buscar
        ) | todas_imagens.filter(
            descricao__icontains=nome_a_buscar
        ) | todas_imagens.filter(
            categoria__icontains=nome_a_buscar
        )
        
        return render(request, 'galeria/buscar.html', {'cards': imagens})
    
    return render(request, 'galeria/buscar.html')

def nova_imagem(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    form = ImagemForms()
    
    if request.method == 'POST':
        form = ImagemForms(request.POST, request.FILES, user=request.user) # request.FILES é necessário para salvar arquivos, como imagens. ImagemForms é um formulário que herda de forms.ModelForm
        
        if form.is_valid():
            form.save() # vantagem de usar forms.ModelForm, é que ele já salva os dados no banco de dados
            messages.success(request, 'Imagem cadastrada com sucesso')
            return redirect('index')
        
    return render(request, 'galeria/nova_imagem.html', {'form': form})
    
def editar_imagem(request, imagem_id):
    if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para acessar essa página')
            return redirect('login')
   
    imagem = get_object_or_404(Imagem, pk=imagem_id)
    
    if request.method == 'POST':
        form = ImagemForms(request.POST, request.FILES, user=request.user, instance=imagem) # O instance é necessario para que os dados que não foram alterados, não sejam perdidos
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Imagem editada com sucesso')
            return redirect('index')
    
    if imagem:
        form = ImagemForms(instance=imagem) # instancia o formulário com os dados da imagem que será editada
        
        return render(request, 'galeria/editar_imagem.html', {'form': form, 'imagem_id': imagem_id}) # imagem_id é passado para o template, para que posso funcionar pq essa URL precisa de um id, foi definido na urls.py. E tambem para achar a imagem que será editada
    
    form = ImagemForms()
    return render(request, 'galeria/editar_imagem.html', {'form': form, 'imagem_id': imagem_id}) # imagem_id é passado para o template, para que posso funcionar pq essa URL precisa de um id, foi definido na urls.py. E tambem para achar a imagem que será editada

def deletar_imagem(request, imagem_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    imagem = get_object_or_404(Imagem, pk=imagem_id)
    imagem.delete()
    return redirect('index')

def favoritar_imagem(request, imagem_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    imagem = get_object_or_404(Imagem, pk=imagem_id)
    favorita, created = Favoritas.objects.get_or_create(user=request.user, imagem=imagem)
    # Se a imagem já foi favoritada, created será False, porque o objeto já existia
    # Se a imagem ainda não foi favoritada, created será True, porque o objeto foi criado agora
    
    if not created:
        # Se a imagem já foi favoritada, removemos a favorita
        favorita.delete()
        
    return redirect('imagem', imagem_id)

def suas_imagens(request, categoria=None):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    if categoria:
        if categoria == 'FAVORITAS':
            imagens_favoritas_ids = Favoritas.objects.filter(user=request.user).values_list('imagem_id', flat=True)
            imagens = Imagem.objects.filter(id__in=imagens_favoritas_ids, user=request.user)
        else:
            imagens = Imagem.objects.filter(categoria=categoria, publicada=True, user=request.user)
    else:
        imagens = Imagem.objects.filter(publicada=True, user=request.user)
        
    imagens_favoritadas_do_usuario = Favoritas.objects.filter(user=request.user).values_list('imagem_id', flat=True)
    
    return render(request, 'galeria/suas_imagens.html', {'cards': imagens, 'imagens_favoritadas_do_usuario': imagens_favoritadas_do_usuario})

def like_imagem(request, image_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    imagem = get_object_or_404(Imagem, id=image_id)
    like, created = Like.objects.get_or_create(user=request.user, imagem=imagem)
    # Se o like já existir, created será False
    # Se o like não existir, created será True

    if created:
        # Incrementa o número de likes se o usuário ainda não tiver curtido a imagem
        imagem.likes += 1
    else:
        # Remove o like e decrementa o número de likes se o usuário já tiver curtido a imagem
        like.delete()
        imagem.likes -= 1

    imagem.save()
    return redirect('imagem', image_id)