from django.shortcuts import render, get_object_or_404, redirect

from apps.galeria.models import Imagem
from apps.galeria.forms import ImagemForms

from django.contrib import messages

# Create your views here.

def index(request, categoria=None):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    if categoria:
        imagens = Imagem.objects.filter(user=request.user, publicada=True, categoria=categoria)
    else:
        # Filtra imagens publicadas do usuário que esta logado no momento
        imagens = Imagem.objects.filter(user=request.user, publicada=True)
    return render(request, 'galeria/index.html', {'cards': imagens})

def imagem(request, imagem_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    imagem = get_object_or_404(Imagem, pk=imagem_id)
    return render(request, 'galeria/imagem.html', {'imagem': imagem})

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
    if imagem.favoritada:
        imagem.favoritada = False
    else:
        imagem.favoritada = True
        
    imagem.save()
    return redirect('index')