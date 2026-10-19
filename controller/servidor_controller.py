from flask import request, render_template, redirect, url_for, session
from models.item import Item
from models.categoria import Categoria
from models.reivindicacao import Reivindicacao
from flask import request, render_template, redirect, url_for, session, flash
from models.sala import Sala



def nova_sala():
    if request.method == 'GET':
        return render_template('admin/servidor/nova_sala.html')

    elif request.method == 'POST':
        dados = {
            "telefone": request.form.get('telefone'),
            "andar": request.form.get('andar'),
            "numero": request.form.get('numero'),
            "descricao": request.form.get('descricao'),
            "predio": request.form.get('predio'),
            "instituicao": session.get('usuario_cnpj_instituicao'),
            "laboratorio": True if request.form.get('laboratorio') else False,
            "sala_de_aula": True if request.form.get('sala_de_aula') else False
        }

        sala = Sala(data=dados)

        if sala.validate(is_new=True):
            if sala.save():
                return redirect(url_for('lista_salas_instituicao'))
            return render_template("admin/errors/500.html"), 500
        
        return render_template(
            'admin/servidor/nova_sala.html',
            sala=sala,
            erros=sala.errors
        ), 400

    else:
        return render_template("admin/errors/405.html"), 405
    

def lista_salas_instituicao():
    cnpj = session.get('usuario_cnpj_instituicao')
    salas = Sala.get_all_by_cnpj(cnpj)
    return render_template(
        'admin/servidor/listar_salas.html',
        salas=salas
    )


def editar_sala(codigo):
    sala = Sala.get_by_codigo(codigo)
    if not sala:
        return render_template("admin/errors/404.html"), 404

    # VERIFICAÇÃO DE SEGURANÇA: Pertence à mesma instituição?
    if sala.instituicao != session.get('usuario_cnpj_instituicao'):
        return render_template("admin/errors/403.html"), 403

    if request.method == 'GET':
        return render_template(
            'admin/servidor/atualizar_sala.html',
            sala=sala
        )

    elif request.method == 'POST':
        try:
            sala.telefone = request.form.get('telefone')
            sala.andar = request.form.get('andar')
            sala.numero = request.form.get('numero')
            sala.descricao = request.form.get('descricao')
            sala.predio = request.form.get('predio')
            sala.laboratorio = True if request.form.get('laboratorio') else False
            sala.sala_de_aula = True if request.form.get('sala_de_aula') else False
        except ValueError as e:
            return render_template(
                'admin/servidor/atualizar_sala.html',
                sala=sala,
                erros=[str(e)]
            ), 400

        if sala.validate(is_new=False):
            if sala.update():
                return redirect(url_for('lista_salas_instituicao'))
            return "Erro ao atualizar sala no banco de dados", 500
        
        return render_template(
            'admin/servidor/atualizar_sala.html',
            sala=sala,
            erros=sala.errors
        ), 400

    else:
        return render_template("admin/errors/405.html"), 405
    

def deletar_sala(codigo):
    sala = Sala.get_by_codigo(codigo)
    if not sala:
        return render_template("admin/errors/404.html"), 404

    # VERIFICAÇÃO DE SEGURANÇA: Pertence à mesma instituição?
    if sala.instituicao != session.get('usuario_cnpj_instituicao'):
        return render_template("admin/errors/403.html"), 403

    if request.method == 'POST':
        if sala.delete():
            return redirect(url_for('lista_salas_instituicao'))
        return render_template("admin/errors/500.html"), 500

    else:
        return render_template("admin/errors/405.html"), 405
    

def detalhes_sala(codigo):
    sala = Sala.get_by_codigo(codigo)
    if not sala:
        return render_template("admin/errors/404.html"), 404

    
    if sala.instituicao != session.get('usuario_cnpj_instituicao'):
        return render_template("admin/errors/403.html"), 403

    return render_template(
        'admin/servidor/detalhes_sala.html',
        sala=sala
    )


def cadastrar_item_encontrado():
    if request.method == "GET":
        categorias = Categoria.get_all_activas()
        return render_template("admin/servidor/novo_item_encontrado.html", categorias=categorias)
        
    elif request.method == "POST":
        data = dict(request.form)
        
        data['instituicao_cnpj'] = session.get('usuario_cnpj_instituicao')
        data['quem_encontrou'] = session.get('usuario_username')
        data['onde_guardado'] = session.get('usuario_sala_codigo')
        data['status'] = 2
        
        novo_item = Item(data=data)
        
        if novo_item.validate(is_new=True):
            if novo_item.save():
                # Opcional: Adicionar uma mensagem de sucesso (flash)
                # flash("Item registrado com sucesso!", "success")
                return redirect(url_for('dashboard_servidor'))
                
            return render_template("admin/errors/500.html"), 500
            
        # CORREÇÃO 3: Se a validação falhar, recarrega a página passando os erros
        categorias = Categoria.get_all_activas()
        return render_template(
            "admin/servidor/novo_item_encontrado.html",
            categorias=categorias,
            erros=novo_item.errors,  # Passa a lista de erros para o HTML exibir
            dados=data               # Repassa os dados para o usuário não ter que digitar tudo de novo
        )
        
    else:
        return render_template("admin/errors/405.html"), 405

def listar_itens_cadastrados():
    cnpj = session.get('usuario_cnpj_instituicao')
    itens = Item.get_all_instituicao(cnpj) 
    return render_template("admin/servidor/lista_itens_encontrado.html", itens=itens) 

def listar_itens_cadastrados_por_categoria(codigo_categoria):
    cnpj = session.get('usuario_cnpj_instituicao')
    categoria = Categoria.get_by_codigo(codigo_categoria)
    itens = Item.get_all_instituicao_by_categoria(cnpj, codigo_categoria) 
    return render_template("admin/servidor/lista_itens_encontrado_por_categoria.html", itens=itens, categoria=categoria) 

def detalhar_item(codigo):
    item = Item.get_by_codigo(codigo)
    if item.instituicao != session.get('usuario_cnpj_instituicao'):
        return render_template("admin/errors/403.html"), 403
    reivindicacoes = Reivindicacao.get_by_item(codigo)
    if item:
        return render_template(
            'admin/servidor/detalhes_item.html',
            item=item,
            reivindicacoes=reivindicacoes
        )
    else:
        return render_template("admin/errors/404.html"), 404


def atualizar_status_item():
    pass



def cadastrar_servidor():
    pass

def desativar_servidor():
    pass


def cadastrar_usuario():
    pass

def desativar_usuario():
    pass




def listar_itens_por_categoria():
    pass

def atualizar_meu_perfil():
    pass

def meu_perfil():
    pass


def alterar_senha():
    pass


def listar_reivindicacoes():
    pass

def visualizar_reivindicacao():
    pass