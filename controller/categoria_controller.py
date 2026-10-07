from models.categoria import Categoria
from flask import render_template, redirect, request, url_for

def nova_categoria():
    if request.method == 'GET':
        return render_template('admin/categoria/nova.html')

    elif request.method == 'POST':
        # Empacota os dados do formulário em um dicionário
        dados = {
            "nome": request.form.get('nome'),
            "descricao": request.form.get('descricao'),
            "ativa": True # Padrão para nova categoria
        }

        # Instancia a classe passando o dicionário data
        categoria = Categoria(data=dados)

        # Valida (is_new=True verifica unicidade de código e slug)
        if categoria.validate(is_new=True):
            categoria.save()
            return redirect(url_for('lista_categorias'))

        # Se houver erros, retorna para o formulário exibindo as mensagens de erro
        return render_template(
            'admin/categoria/nova.html',
            categoria=categoria,
            erros=categoria.errors
        ), 400

    else:
        return "Método não permitido", 405

def listar_categorias():
    categorias = Categoria.get_all()
    return render_template('admin/categoria/lista.html', categorias=categorias)

def atualizar_categoria(codigo):
    categoria = Categoria.get_by_codigo(codigo)
    if not categoria:
        return "Categoria não encontrada", 404

    if request.method == 'GET':
        return render_template('admin/categoria/atualizar.html', categoria=categoria)

    elif request.method == 'POST':
        # Atualiza os dados através das propriedades (que modificam o self.data interno)
        try:
            categoria.nome = request.form.get('nome')
            categoria.descricao = request.form.get('descricao')
            categoria.ativa = True if request.form.get('ativa') else False
        except ValueError as e:
            # Caso algum setter lance uma exceção (ex: valor vazio)
            return render_template(
                'admin/categoria/atualizar.html',
                categoria=categoria,
                erros=[str(e)]
            ), 400

        # Valida a atualização (is_new=False pois já existe no banco)
        if categoria.validate(is_new=False):
            categoria.update()
            return redirect(url_for('lista_categorias'))

        # Se houver erros de validação
        return render_template(
            'admin/categoria/atualizar.html',
            categoria=categoria,
            erros=categoria.errors
        ), 400

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