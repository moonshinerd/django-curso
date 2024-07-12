from django.shortcuts import render,redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User
from django.contrib import auth, messages

def login(request):
    forms = LoginForms()

    if request.method == 'POST':
        forms = LoginForms(request.POST)
        
        if forms.is_valid():
            nome=forms['nome_login'].value()
            senha=forms['senha'].value()

        usuario = auth.authenticate(
            request,
            username= nome,
            password=senha
        )

        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f"{nome} logado com sucesso!")
            return redirect('index')
        else:
            messages.error(request,"Erro ao efetuar login")
            return redirect('login')

    return render(request,"usuarios/login.html", {"form":forms})

def cadastro(request):
    forms = CadastroForms()

    if request.method == 'POST':
        forms = CadastroForms(request.POST)
        if forms.is_valid():
            
            
            nome=forms["nome_cadastro"].value()
            email=forms["email"].value()
            senha=forms["senha_1"].value()

            if User.objects.filter(username = nome).exists():
                messages.error(request, "Usuário já existente")
                return redirect('cadastro')

            usuario = User.objects.create_user(
                username = nome,
                email = email,
                password = senha
            )
            usuario.save()
            messages.success(request, "Cadastro efetuado com sucesso")
            return redirect('login')

    return render(request,"usuarios/cadastro.html", {'form': forms})

def logout(request):
    auth.logout(request)
    messages.success(request,"Logout efetuado com sucesso!")
    return redirect('login')