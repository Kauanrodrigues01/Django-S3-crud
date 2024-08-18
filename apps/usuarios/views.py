from django.shortcuts import render, redirect

from apps.usuarios.forms import LoginForms, CadastroForms

from django.contrib.auth.models import User

from django.contrib import auth, messages

# Create your views here.
def login(request):
    form = LoginForms()
    
    if request.method == 'POST':
        form = LoginForms(request.POST)
        
        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()
            
            usuario = auth.authenticate(request, username=nome, password=senha) # Verifica se o usuário existe e se a senha está correta, ele pega os dados da tabela auth_user do banco de dados
            
            if usuario is not None:
                auth.login(request, usuario)
                messages.success(request, f'{nome} logado com sucesso!')
                return redirect('index')
            else:
                messages.error(request, 'Usuário ou senha inválidos')
                return redirect('login')
    
    return render(request, 'usuarios/login.html', {'form': form})

def cadastro(request):
    form = CadastroForms()
    
    if request.method == 'POST':
        form = CadastroForms(request.POST)
        
        if form.is_valid():
            nome = form['nome_cadastro'].value()
            email = form['Email'].value()
            senha = form['senha'].value()
            confirmar_senha = form['confirmar_senha'].value()
            
            # Verificar se as senhas são iguais
            if senha != confirmar_senha:
                messages.error(request, 'As senhas não são iguais')
                return redirect('cadastro')
            
            # Verifica se já existe um cadastro com aquele email
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email já cadastrado')
                return redirect('cadastro')
            
            # Verificar se o usuário já existe
            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existe')
                return redirect('cadastro')
            
            # Criar o novo usuário
            usuario = User.objects.create_user(
                username=nome, 
                email=email, 
                password=senha
            )
            usuario.save()
            messages.success(request, f'{nome} cadastrado com sucesso!')
            return redirect('login')
        
    return render(request, 'usuarios/cadastro.html', {'form': form})

def logout(request):
    auth.logout(request) # Função que faz o logout do usuário, ou seja, ele deixa de estar logado
    messages.success(request, 'Deslogado com sucesso!')
    return redirect('login') # Redireciona para a rota chamada 'login'

def perfil(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Tem que estar logado para acessar está página')
        return redirect('login')
    
    nome_usario = request.user.username
    email_usuario = request.user.email
    senha = request.user.password
    senha_usuario = int((len(senha) / 6)) * '*' 
    
    return render(request, 'usuarios/perfil.html', {'nome_usario': nome_usario, 'email_usuario': email_usuario, 'senha_usuario': senha_usuario})

def editar_perfil(request):
    usuario = request.user

    if request.method == 'POST':
        formCadastro = CadastroForms(request.POST)
        if formCadastro.is_valid():
            # Atualize o usuário com os dados do formulário
            
            usuario.username = formCadastro.cleaned_data['nome_cadastro'] # cleaned_data é um dicionário que contém os dados do formulário, neste caso, ele pega o valor do campo 'nome_cadastro'
            usuario.email = formCadastro.cleaned_data['Email']
            
            senha = formCadastro.cleaned_data['senha']
            confirmar_senha = formCadastro.cleaned_data['confirmar_senha']
            
            if senha == confirmar_senha:
                usuario.set_password(senha) # set_password é um método do objeto User que criptografa a senha e salva de forma segura no banco de dados
            else:
                formCadastro.add_error('confirmar_senha', 'As senhas não são iguais.') # Adiciona um erro ao campo 'confirmar_senha'
                return render(request, 'usuarios/editar_perfil.html', {'form': formCadastro}) # Retorna o formulário com o erro
            
            usuario.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('login')
        else:
            return render(request, 'usuarios/editar_perfil.html', {'form': formCadastro})
    else:
        initial_data = { # Dicionário com os dados iniciais do formulário
            'nome_cadastro': usuario.username,
            'Email': usuario.email,
        }
        formCadastro = CadastroForms(initial=initial_data) # Cria o formulário com os dados iniciais

    return render(request, 'usuarios/editar_perfil.html', {'form': formCadastro})