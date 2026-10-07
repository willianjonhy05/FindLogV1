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
        # 1. Empacota os dados recebidos do formulário
        tipo_usuario = int(request.form.get('tipo_usuario', 1))
        
        dados = {
            "nome": request.form.get('nome'),
            "email": request.form.get('email'),
            "senha": request.form.get('senha'),
            "cpf": request.form.get('cpf'),
            "data_nascimento": request.form.get('data_nascimento'),
            "instituicao": request.form.get('instituicao_cnpj'),
            "tipo_usuario": tipo_usuario,
            "telefone": request.form.get('telefone'),
            "sala": request.form.get('sala_codigo') if tipo_usuario == 3 else None
        }

        # 2. Instancia o usuário (o username será gerado automaticamente)
        usuario = Usuario(data=dados)

        # 3. Trata o upload da foto de perfil, se houver
        arquivo_foto = request.files.get('foto_perfil')
        if arquivo_foto and arquivo_foto.filename != '':
            caminho_foto = salvar_foto_perfil(arquivo_foto, usuario.username)
            if caminho_foto:
                usuario.foto_perfil = caminho_foto

        # 4. Valida os dados (is_new=True verifica unicidade de CPF e username)
        if usuario.validate(is_new=True):
            if usuario.save():
                return redirect(url_for('lista_usuarios'))
            return "Erro ao salvar usuário no banco de dados", 500

        # Se houver erros, retorna para o formulário exibindo as mensagens
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        return render_template(
            'admin/usuario/novo.html',
            usuario=usuario,
            instituicoes=instituicoes,
            salas=salas,
            erros=usuario.errors
        ), 400

    else:
        return "Método não permitido", 405


def lista_usuarios():
    usuarios = Usuario.get_all()
    return render_template(
        'admin/usuario/lista.html',
        usuarios=usuarios
    )


def editar_usuario(username):
    usuario = Usuario.get_by_username(username)
    if not usuario:
        return "Usuário não encontrado", 404

    if request.method == 'GET':
        instituicoes = Instituicao.listar_instituicoes_ativas()
        salas = Sala.get_all()
        return render_template(
            'admin/usuario/editar.html',
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
            return "Erro ao atualizar usuário no banco de dados", 500

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
        return "Método não permitido", 405


def deletar_usuario(username):
    usuario = Usuario.get_by_username(username)
    if not usuario:
        return "Usuário não encontrado", 404

    if request.method == 'POST':
        if usuario.delete():
            return redirect(url_for('lista_usuarios'))
        return "Erro ao deletar usuário", 500

    else:
        return "Método não permitido", 405


def visualizar_usuario(username):
    usuario = Usuario.get_by_username(username)
    if usuario:
        return render_template(
            'admin/usuario/detalhes.html',
            usuario=usuario
        )
    else:
        return "Usuário não encontrado", 404