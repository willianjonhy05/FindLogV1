from flask import render_template, request, redirect, url_for, session
from models.item import Item
from models.categoria import Categoria
from models.instituicao import Instituicao
from models.sala import Sala
from models.usuario import Usuario
from utils.upload import salvar_foto_item
import os
from werkzeug.utils import secure_filename




def novo_item():
    if request.method == 'GET':
        categorias = Categoria.get_all()
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        usuarios = Usuario.get_all()
        return render_template(
            'admin/item/novo.html',
            categorias=categorias,
            instituicoes=instituicoes,
            salas=salas,
            usuarios=usuarios
        )

    elif request.method == 'POST':
        # 1. Coleta os dados do formulário
        status_val = int(request.form.get('status', 1))
        
        dados = {
            "cor": request.form.get('cor'),
            "tamanho": request.form.get('tamanho'),
            "material": request.form.get('material'),
            "detalhes": request.form.get('detalhes'),
            "status": status_val,
            "categoria": request.form.get('categoria_codigo'),
            "instituicao": request.form.get('instituicao_cnpj'),
            "onde_guardado": request.form.get('onde_guardado_codigo') if status_val == 3 else None,
            "onde_encontrado": request.form.get('onde_encontrado'),
            "quem_encontrou": request.form.get('quem_encontrou_username') or session.get('usuario_username'),
            "dono": request.form.get('dono_username') or None,
            "data_devolucao": request.form.get('data_devolucao') or None
        }

        # 2. Instancia o item (o código único é gerado automaticamente no __init__)
        item = Item(data=dados)

        # 3. Trata o upload da foto do item, se houver
        arquivo_foto = request.files.get('foto')
        if arquivo_foto and arquivo_foto.filename != '':
            caminho_foto = salvar_foto_item(arquivo_foto, item.codigo)
            if caminho_foto:
                item.foto = caminho_foto

        # 4. Valida os dados (is_new=True verifica unicidade do código)
        if item.validate(is_new=True):
            if item.save():
                return redirect(url_for('lista_itens'))
            return "Erro ao salvar item no banco de dados", 500

        # Se houver erros, recarrega o formulário enviando as dependências
        categorias = Categoria.get_all()
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        usuarios = Usuario.get_all()
        return render_template(
            'admin/item/novo.html',
            item=item,
            categorias=categorias,
            instituicoes=instituicoes,
            salas=salas,
            usuarios=usuarios,
            erros=item.errors
        ), 400

    else:
        return "Método não permitido", 405


def lista_itens():
    itens = Item.get_all()
    return render_template(
        'admin/item/lista.html',
        itens=itens
    )


def editar_item(codigo):
    item = Item.get_by_codigo(codigo)
    if not item:
        return "Item não encontrado", 404

    if request.method == 'GET':
        categorias = Categoria.get_all()
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        usuarios = Usuario.get_all()
        return render_template(
            'admin/item/editar.html',
            item=item,
            categorias=categorias,
            instituicoes=instituicoes,
            salas=salas,
            usuarios=usuarios
        )

    elif request.method == 'POST':
        try:
            status_val = int(request.form.get('status', item.status))
            
            # Atualiza os dados através das propriedades (setters)
            item.cor = request.form.get('cor')
            item.tamanho = request.form.get('tamanho')
            item.material = request.form.get('material')
            item.detalhes = request.form.get('detalhes')
            item.status = status_val
            item.categoria = request.form.get('categoria_codigo')
            item.instituicao = request.form.get('instituicao_cnpj')
            item.onde_encontrado = request.form.get('onde_encontrado')
            item.quem_encontrou = request.form.get('quem_encontrou_username') or None
            item.dono = request.form.get('dono_username') or None
            item.data_devolucao = request.form.get('data_devolucao') or None
            
            if status_val == 3:
                item.onde_guardado = request.form.get('onde_guardado_codigo')
            else:
                item.onde_guardado = None

        except ValueError as e:
            categorias = Categoria.get_all()
            instituicoes = Instituicao.listar_instituicoes_ativas()
            salas = Sala.get_all()
            usuarios = Usuario.get_all()
            return render_template(
                'admin/item/editar.html',
                item=item,
                categorias=categorias,
                instituicoes=instituicoes,
                salas=salas,
                usuarios=usuarios,
                erros=[str(e)]
            ), 400

        # Trata o upload de nova foto, caso enviada
        arquivo_foto = request.files.get('foto')
        if arquivo_foto and arquivo_foto.filename != '':
            caminho_foto = salvar_foto_item(arquivo_foto, item.codigo)
            if caminho_foto:
                item.foto = caminho_foto

        # Valida a atualização (is_new=False pois o item já existe)
        if item.validate(is_new=False):
            if item.update():
                return redirect(url_for('lista_itens'))
            return "Erro ao atualizar item no banco de dados", 500

        # Se houver erros de validação
        categorias = Categoria.get_all()
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        usuarios = Usuario.get_all()
        return render_template(
            'admin/item/editar.html',
            item=item,
            categorias=categorias,
            instituicoes=instituicoes,
            salas=salas,
            usuarios=usuarios,
            erros=item.errors
        ), 400

    else:
        return "Método não permitido", 405


def deletar_item(codigo):
    item = Item.get_by_codigo(codigo)
    if not item:
        return "Item não encontrado", 404

    if request.method == 'POST':
        if item.delete():
            return redirect(url_for('lista_itens'))
        return "Erro ao deletar item", 500

    else:
        return "Método não permitido", 405


def visualizar_item(codigo):
    item = Item.get_by_codigo(codigo)
    if item:
        return render_template(
            'admin/item/detalhes.html',
            item=item
        )
    else:
        return "Item não encontrado", 404