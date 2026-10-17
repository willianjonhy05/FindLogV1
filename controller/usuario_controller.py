from flask import render_template, request, redirect, url_for, session
from models.usuario import Usuario
from models.instituicao import Instituicao
from models.sala import Sala
from utils.upload import salvar_foto_perfil, allowed_file

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
    

def alterar_senha():
    username_logado = session.get('usuario_username')
    if not username_logado:
        return redirect(url_for('login'))
        
    usuario = Usuario.get_by_username(username_logado)
    if not usuario:
        return render_template("admin/errors/404.html"), 404
        
    if request.method == 'GET':
        return render_template('admin/usuario/alterar_senha.html', usuario=usuario)
        
    elif request.method == 'POST':
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        erros = {}
        
        # Validações iniciais
        if not senha_atual or not nova_senha or not confirmar_senha:
            erros['geral'] = "Todos os campos são obrigatórios."
        elif nova_senha != confirmar_senha:
            erros['confirmar_senha'] = "As senhas novas não coincidem."
            
        if not erros:
            sucesso, mensagem = usuario.alterar_senha(senha_atual, nova_senha)
            if sucesso:
                # Opcional: você pode adicionar uma mensagem flash aqui se utilizar no projeto
                return redirect(url_for('meu_perfil'))
            else:
                erros['senha_atual'] = mensagem
                
        return render_template(
            'admin/usuario/alterar_senha.html',
            usuario=usuario,
            erros=erros
        ), 400
        
    else:
        return render_template("admin/errors/405.html"), 405


def editar_perfil():
    username_logado = session.get('usuario_username')
    if not username_logado:
        return redirect(url_for('login'))
        
    usuario = Usuario.get_by_username(username_logado)
    if not usuario:
        return render_template("admin/errors/404.html"), 404
        
    if request.method == 'GET':
        return render_template('admin/usuario/editar_perfil.html', usuario=usuario)
        
    elif request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        data_nascimento = request.form.get('data_nascimento')
        
        erros = {}
        if not nome or not email:
            erros['geral'] = "Nome e e-mail são obrigatórios."
            
        # Processamento da Foto de Perfil utilizando a sua função utilitária
        file = request.files.get('foto_perfil')
        foto_path = None
        
        if file and file.filename != '':
            # Chama a função do seu upload.py
            foto_path = salvar_foto_perfil(file, username_logado)
            if not foto_path:
                erros['foto'] = "Formato de imagem inválido. Utilize PNG, JPG, JPEG ou WEBP."

        if not erros:
            dados_atualizados = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "data_nascimento": data_nascimento
            }
            
            # Se a foto foi salva com sucesso, adiciona o caminho relativo aos dados
            if foto_path:
                dados_atualizados["foto_perfil"] = foto_path
                
            sucesso, mensagem = usuario.atualizar_perfil(dados_atualizados)
            if sucesso:
                return redirect(url_for('meu_perfil'))
            else:
                erros['geral'] = mensagem
                
        return render_template(
            'admin/usuario/editar_perfil.html',
            usuario=usuario,
            erros=erros
        ), 400
        
    else:
        return render_template("admin/errors/405.html"), 405