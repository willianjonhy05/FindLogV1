
from models.categoria import Categoria
from flask import render_template, redirect, request, url_for

def nova_categoria():
    if request.method == 'GET':
        return render_template('admin/categoria/nova.html')

    elif resquest.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')

        categoria = Categoria(
            nome=nome,
            descricao=descricao
        )

        if categoria.save():
            return redirect(url_for('lista_categorias'))

    else:
        return "Método não permitido", 405

def listar_categorias():
    categorias = Categoria.get_all()
    return render_template('admin/categoria/lista.html', categorias=categorias)

def atualizar_categoria():
    categoria = Categoria.get_by_codigo(codigo)
    if not categoria:
        return "Categoria não encontrada", 404

    if request.method == 'GET':
        return render_template('admin/categoria/atualizar.html', categoria=categoria)

    elif request.method == 'POST':
        novo_nome = request.form.get('nome')        
        nova_descricao = request.form.get('descricao')
        ativo_form = True if request.form.get('ativa') else False

        categoria.nome = novo_nome
        categoria.descricao = nova_descricao
        categoria.ativa = ativo_form

        categoria.update()
        return redirect(url_for('lista_categorias'))


    else:
        return "Método não permitido", 405



def apagar_categoria(codigo):
    categoria = Categoria.get_by_codigo(codigo)
    if categoria:
        categoria.delete()
        return redirect(url_for('lista_categorias'))
    return "Categoria não encontrada", 404

def visualizar_categoria(codigo):
    categoria = Categoria.get_by_codigo(codigo)
    if categoria:
        return render_template('admin/categoria/detalhes.html', categoria=categoria)
    else:
        return "Categoria não encontrada", 404