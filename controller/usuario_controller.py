from flask import render_template, request, redirect, url_for
from models.usuario import Usuario
from models.instituicao import Instituicao
from models.sala import Sala
from utils.upload import salvar_foto_perfil

def novo_usuario():
    if request.method == 'GET':
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        return render_template(
            'admin/usuario/novo.html',
            instituicoes=instituicoes,
            salas=salas
        )

    elif request.method == 'POST':
        tipo_usuario = int(request.form.get('tipo_usuario', 1))
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        # Validação básica de senhas coincidentes antes de instanciar
        erros_customizados = {}
        if senha != confirmar_senha:
            erros_customizados['confirmar_senha'] = "As senhas não coincidem."

        dados = {
            "nome": request.form.get('nome'),
            "email": request.form.get('email'),
            "senha": senha,
            "cpf": request.form.get('cpf'),
            "data_nascimento": request.form.get('data_nascimento'),
            "instituicao": request.form.get('instituicao_cnpj'),
            "tipo_usuario": tipo_usuario,
            "telefone": request.form.get('telefone'),
            "sala": request.form.get('sala_codigo') if tipo_usuario == 3 else None
        }

        usuario = Usuario(data=dados)
        
        # Se houver erro de senha ou de validação do modelo, unimos os erros
        if erros_customizados or not usuario.validate(is_new=True):
            if erros_customizados:
                # Se o objeto usuario já tiver erros, unimos, senão criamos o dicionário
                if hasattr(usuario, 'errors') and isinstance(usuario.errors, dict):
                    usuario.errors.update(erros_customizados)
                else:
                    usuario.errors = erros_customizados

            instituicoes = Instituicao.listar_instituicoes_ativas()
            salas = Sala.get_all()
            return render_template(
                'admin/usuario/novo.html',
                usuario=usuario,
                instituicoes=instituicoes,
                salas=salas,
                erros=usuario.errors
            ), 400

        # Tratamento do upload da foto de perfil
        arquivo_foto = request.files.get('foto_perfil')
        if arquivo_foto and arquivo_foto.filename != '':
            caminho_foto = salvar_foto_perfil(arquivo_foto, usuario.username)
            if caminho_foto:
                usuario.foto_perfil = caminho_foto

        if usuario.save():
            return redirect(url_for('lista_usuarios'))
        
        return render_template("admin/errors/500.html"), 500

    else:
        return render_template("admin/errors/405.html"), 405

def lista_usuarios():
    usuarios = Usuario.get_all()
    return render_template(
        'admin/usuario/lista.html',
        usuarios=usuarios
    )


def editar_usuario(username):
    usuario = Usuario.get_by_username(username)
    if not usuario:
        return render_template("admin/errors/404.html"), 404

    if request.method == 'GET':
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        return render_template(
            'admin/usuario/atualizar.html',
            usuario=usuario,
            instituicoes=instituicoes,
            salas=salas
        )

    elif request.method == 'POST':
        try:
            tipo_usuario = int(request.form.get('tipo_usuario', usuario.tipo_usuario))
            
            # Atualiza os dados através das propriedades (setters)
            usuario.nome = request.form.get('nome')
            usuario.email = request.form.get('email')
            usuario.cpf = request.form.get('cpf')
            usuario.data_nascimento = request.form.get('data_nascimento')
            usuario.instituicao = request.form.get('instituicao_cnpj')
            usuario.tipo_usuario = tipo_usuario
            usuario.telefone = request.form.get('telefone')
            usuario.ativo = True if request.form.get('ativo') else False
            
            # Trata a sala com base no tipo de usuário
            if tipo_usuario == 3:
                usuario.sala = request.form.get('sala_codigo')
            else:
                usuario.sala = None

            # Se uma nova senha foi preenchida, atualiza
            nova_senha = request.form.get('senha')
            if nova_senha and nova_senha.strip():
                usuario.senha = nova_senha

        except ValueError as e:
            instituicoes = Instituicao.listar_instituicoes_ativas()
            salas = Sala.get_all()
            return render_template(
                'admin/usuario/editar.html',
                usuario=usuario,
                instituicoes=instituicoes,
                salas=salas,
                erros=[str(e)]
            ), 400

        # Trata o upload de nova foto de perfil, caso enviada
        arquivo_foto = request.files.get('foto_perfil')
        if arquivo_foto and arquivo_foto.filename != '':
            caminho_foto = salvar_foto_perfil(arquivo_foto, usuario.username)
            if caminho_foto:
                usuario.foto_perfil = caminho_foto

        # Valida a atualização (is_new=False pois o usuário já existe)
        if usuario.validate(is_new=False):
            if usuario.update():
                return redirect(url_for('lista_usuarios'))
            return render_template("admin/errors/500.html"), 500

        # Se houver erros de validação
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        return render_template(
            'admin/usuario/editar.html',
            usuario=usuario,
            instituicoes=instituicoes,
            salas=salas,
            erros=usuario.errors
        ), 400

    else:
        return render_template("admin/errors/405.html"), 405


def deletar_usuario(username):
    usuario = Usuario.get_by_username(username)
    if not usuario:
        return render_template("admin/errors/404.html"), 404

    if request.method == 'POST':
        if usuario.delete():
            return redirect(url_for('lista_usuarios'))
        return render_template("admin/errors/500.html"), 500

    else:
        return render_template("admin/errors/405.html"), 405


def visualizar_usuario(username):
    usuario = Usuario.get_by_username(username)
    cpnj_instituicao = usuario.instituicao    
    context = {
        "usuario": usuario,
        "cpnj_instituicao": cpnj_instituicao
    }

    if usuario:
        return render_template(
            'admin/usuario/detalhes.html',
            **context
        )
    else:
        return render_template("admin/errors/404.html"), 404