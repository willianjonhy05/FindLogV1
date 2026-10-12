from flask import render_template, request
from models.instituicao import Instituicao
from models.categoria import Categoria
from models.usuario import Usuario
from models.sala import Sala
from models.item import Item


def index():
    return render_template('public/index.html')


def dashboard_admin():
    # Criação do dicionário com os dados
    context = {
        "total_instituicoes": Instituicao.quantidade(),
        "total_categorias": Categoria.contar_total(),
        "total_usuarios": Usuario.contar_total(),
        "total_salas": Sala.contar_total(),  # Incluído para a template não quebrar
        "total_itens": Item.contar_total()    # Incluído para a template não quebrar
    }
    
    # O operador ** desempacota o dicionário como variáveis nomeadas (kwarg)
    return render_template('admin/admin/dashboard.html', **context)

# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     elif request.method == 'POST':
#         email = request.form.get("email")
#         senha = request.form.get("senha")
#         return "Login realizado com sucesso!"
#     else:
#         return "Método não permitido", 405
