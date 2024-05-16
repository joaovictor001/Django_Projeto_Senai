from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def formulario_novo_user(request):
    return render(request,'cad_user.html')

def salvar_usuario(request):
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    print(usuario,email,senha)


    usuario_logado = request.user.username
    if(usuario != None and usuario != '' and email != None and email != '' and senha != None and senha != ''):
        try:
            tem_usuario = User.objects.get(username=usuario)
            if(tem_usuario):
                message.info(request, "Usuario ja existe, tente outro.")
                return render(request, 'cad_user.html')
        except User.DoesNoExit:
            dados_usuario = User.objects.create_user(username=usuario, email=email, password=senha)
            dados_usuario.save()
            message.info(request, "Usuario salvo com sucesso")
            return render(request, 'cad_user.html', {'usuario_logado':usuario_logado})
