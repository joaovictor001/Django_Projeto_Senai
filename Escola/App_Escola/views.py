from django.shortcuts import render
from hashlib import sha256
from .models import Professor,Turma,Atividade
from django.db import connection, transaction
from django.contrib import messages

def abre_index(request):
 return render(request, 'login.html')

def initial_poopulation():
    print("Vou Popular")

    cursor = connection.cursor()

    senha = "123456"
    senha_armazenar = sha256(senha)

    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES"
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama','barak.obama@gmail.com', '"+senha_armazenar+ "'),"
    insert_sql_professor = insert_sql_professor + "('Prof. Angela Merkel', 'angela.markel@gmail.com', '" + senha_armazenar+"'),"
    senha_armazenar = senha_armazenar + "('Prof. Xi Jinping', 'xi.jinping@gmail.com','"+senha_armazenar+"')"

    cursor.execute(insert_sql_professor)
    transaction.atomic()

    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES "
    insert_sql_turma = insert_sql_turma + "('1o Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma = insert_sql_turma + "('2o Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3o Semestre - Desenvolvimento de Sistemas', 3),"

    cursor.execute(insert_sql_turma)
    transaction.atomic()

    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade + insert_sql_atividade + "('Apresentar Fundamentos de Programação', 1 ),"
    insert_sql_atividade + insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
    insert_sql_atividade + insert_sql_atividade + "('Apresentar conceitos de Gerenciamentos de Projetos',3)"

    cursor.execute(insert_sql_atividade)
    transaction.atomic()

    print("Populei")