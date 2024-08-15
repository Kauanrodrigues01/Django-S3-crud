from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

def verificar_senha(senha):
    errors = []
    if len(senha) < 8:
        errors.append("Senha deve ter pelo menos 8 caracteres.")
    if not re.search(r'[A-Z]', senha):
        errors.append("Senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r'[a-z]', senha):
        errors.append("Senha deve conter pelo menos uma letra minúscula.")
    if not re.search(r'[0-9]', senha):
        errors.append("Senha deve conter pelo menos um número.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        errors.append("Senha deve conter pelo menos um caractere especial.")
    if errors:
        raise ValidationError(errors)


def verificar_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def verificar_nome_usuario(nome):
    if ' ' in nome:
        return 'Nome de usuário não pode ter espaços'
    if len(nome) < 3:
        return 'Nome de usuário deve ser maior que 3 caracteres.'
    if len(nome) > 30:
        return 'Nome de usuário deve ser menor que 30 caracteres.'
    if not re.match(r'^[\w.@+-]+$', nome):
        return 'Nome de usuário contém caracteres inválidos.'
    
    return True

class LoginForms(forms.Form):
    nome_login=forms.CharField(
        label='Nome de usuário',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'EX: João da Silva',
                'class': 'form-control',
            }
        )
    )
    senha = forms.CharField(
        label='Senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Digite sua senha',
                'class': 'form-control'
            }
        ) # Para não mostrar a senha
    )
    
    def clean_nome_login(self):
        nome = self.cleaned_data.get('nome_login')
        
        # Verificar se o nome de usuário é válido
        verificacao_nome = verificar_nome_usuario(nome)
        if verificacao_nome is not True:
            raise ValidationError(verificacao_nome)
        
        return nome
    
class CadastroForms(forms.Form):
    nome_cadastro=forms.CharField(
        label='Nome de usuário',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'EX: João da Silva',
                'class': 'form-control',
            }
        )
    )
    Email=forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'EX: joao231@gamil.com',
                'class': 'form-control',
            }
        )
    )
    senha = forms.CharField(
        label='Senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Digite sua senha',
                'class': 'form-control'
            }    
        ) # Para não mostrar a senha
    )
    confirmar_senha = forms.CharField(
        label='Confirmar senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirme sua senha',
                'class': 'form-control'
            }
        ) # Para não mostrar a senha
    )
    
    def clean_nome_cadastro(self):
        nome = self.cleaned_data.get('nome_cadastro')
        if nome:
            nome = nome.strip()
            verificacao_nome = verificar_nome_usuario(nome)
            if verificacao_nome is not True:
                raise ValidationError(verificacao_nome)

        return nome

    def clean_Email(self):
        email = self.cleaned_data.get('Email')
        if not verificar_email(email):
            raise ValidationError('Email inválido')

        return email

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        verificar_senha(senha)  # Ajustado para lançar ValidationError diretamente

        return senha
    
    def clean(self):
        cleaned_data = super().clean() # Chama o método clean da classe pai, para garantir que todos os campos foram validados
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        
        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', 'As senhas não são iguais.') # a função add_error adiciona um erro ao campo 'confirmar_senha'

        
        
        