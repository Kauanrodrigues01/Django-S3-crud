from django.shortcuts import render, get_object_or_404, redirect

from apps.galeria.models import Imagem
from apps.galeria.forms import ImagemForms

from django.contrib import messages

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    # Filtra imagens publicadas do usuário que esta logado no momento
    imagens = Imagem.objects.filter(user=request.user, publicada=True)
    return render(request, 'galeria/index.html', {'cards': imagens})

def imagem(request, imagem_id):
    imagem = get_object_or_404(Imagem, pk=imagem_id)
    return render(request, 'galeria/imagem.html', {'imagem': imagem})

def buscar(request):
    
    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado para acessar essa página')
        return redirect('login')
    
    todas_imagens = Imagem.objects.all().filter(publicada=True)
    
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar'] # pega o valor do campo de busca, na url
        
        if nome_a_buscar:
            imagens = todas_imagens.filter(nome__icontains=nome_a_buscar) | todas_imagens.filter(descricao__icontains=nome_a_buscar) | todas_imagens.filter(categoria__icontains=nome_a_buscar)
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
    
def editar_imagem(request, id):
    pass

def deletar_imagem(resquest, id):
    pass