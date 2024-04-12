from django.shortcuts import render
from hashlib import sha256
from .models import Professor,Turma,Atividade
from django.db import connection, transaction
from django.contrib import messages
from django.http import HttpResponse

def initial_population():
    print("Vou Popular")

    cursor = connection.cursor()

    senha = "123456"
    senha_armazenar = sha256(senha.encode()).hexdigest()
    print(senha_armazenar)
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama','barak.obama@gmail.com', '"+senha_armazenar+ "'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Angela Merkel', 'angela.markel@gmail.com', '" + senha_armazenar+"'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com','"+senha_armazenar+"')"

    cursor.execute(insert_sql_professor)
    transaction.atomic()


    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES "
    insert_sql_turma = insert_sql_turma + "('1o Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2o Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3o Semestre - Desenvolvimento de Sistemas', 3)"

    cursor.execute(insert_sql_turma)
    transaction.atomic()

    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade + insert_sql_atividade + "('Apresentar Fundamentos de Programação', 1 ),"
    insert_sql_atividade + insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
    insert_sql_atividade + insert_sql_atividade + "('Apresentar conceitos de Gerenciamentos de Projetos',3)"

    cursor.execute(insert_sql_atividade)
    transaction.atomic()

    print("Populei")


def abre_index(request):
    dado_pesquisa = 'Obama'

    verifica_populado = Professor.objects.filter(nome__icontains=dado_pesquisa)
    
    if not verifica_populado.exists():
        print("Não está populado")
        initial_population()  # Chama a função para popular o banco de dados com dados iniciais
    else:
        print("Achei Obama", verifica_populado)

    return render(request, 'login.html')

    

def enviar_login(request):
    if(request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome","senha","id")
        print("Dados do Professor" , dados_professor)
        #if len(dados_professor) > 0
        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado  = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            if(senha == senha_criptografada):

                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turmas.objects.filter(id_professor=id_logado)
                print("Turma do Professor", turmas_do_professor)
                return render (request , 'Cons_Turma_Lista.html', {'usuario_logado': usuario_logado,
                                                                   'turmas_do_professor':turmas_do_professor,
                                                                   'id_logado': id_logado})
            else:
                menssges.info(request, 'Usuario ou senha incorretos. Tente novamente. ')
                return render(request,'login.html')
            
        messages.info(request, "Olá"+ email+ ",seja bem-vindo! Perebemos que voce é novo por aqui. Complete seu cadastro.")
        return render(request, 'cadastro.html',{'login':email})


def confirmar_cadastro(request):
    if(request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()

        grava_professor = Professor(
            nome=nome,
            email=email,
            senha =senha_criptografada
        )    
        grava_professor.save()

        mensagem = "OLÁ PROFESSOR"+ nome +",SEJA BEM VINDO"
        return HttpResponse(mensagem)

def cad_turma(request, id_professor):
    usuario_logado = Professor.objects.filter(id=idprofessor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']

    return render(request, 'Cad_Turma.html', {'usuario_logado': usuario_logado, 'id_logado': id_professor})

def salvar_turma_nova(request):
    nome_turma = request.POST.get('nome_turma')
    id_professor = request.POST.get('id_professor')
    professor = Professor.objects.get(id=id_professor)
    grava_turma = Turma(
        nome_turma = nome_turma,
        id_professor = professor
    )
    grava_turma.save()
    messages.info(request, 'Turma' + nome_turma+'cadastor com sucesso. ')

    return redirect('lista_turma', id_professor=id_professor)


def lista_turma(request, id_professor):
    dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    id_logado = dados_professor[0]
    id_logado = id_logado['id']
    turmas_do_professor = Turmas.objects.filter(id_professor=id_logado)
    return render(request, 'Cons_Turma_Lista.html',
                            {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor,
                            'id_logado': id_logado})