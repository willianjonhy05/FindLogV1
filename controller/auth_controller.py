from flask import render_template, request, redirect, url_for, session
from models.usuario import Usuario

def login():
    if request.method == 'GET':
        # Se já estiver logado, redireciona com base no tipo dele
        if 'usuario_username' in session:
            return _redirecionar_por_tipo(session.get('usuario_tipo'))
        return render_template('login.html')

    elif request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            return render_template('login.html', erro="Preencha todos os campos."), 400

        # Busca o usuário pelo username
        usuario = Usuario.get_by_email(email)

        # Valida se o usuário existe, está ativo e se a senha está correta
        if usuario and usuario.ativo and usuario.verificar_senha(senha):
            # Salva os dados essenciais na sessão do Flask
            session['usuario_email'] = usuario.email
            session['usuario_username'] = usuario.username
            session['usuario_nome'] = usuario.primeiro_nome
            session['usuario_tipo'] = int(usuario.tipo_usuario)
            session['usuario_foto'] = usuario.foto_perfil
            session['usuario_cnpj_instituicao'] = usuario.instituicao

            if usuario.tipo_usuario == 3:
                session['usuario_sala_codigo'] = usuario.sala_codigo
            

            return _redirecionar_por_tipo(usuario.tipo_usuario)

        return render_template('login.html', erro="Usuário ou senha inválidos."), 401

    else:
        return "Método não permitido", 405


def _redirecionar_por_tipo(tipo_usuario):
    """Função auxiliar para centralizar as rotas de redirecionamento por tipo"""
    # Converte para int caso venha como string do banco, garantindo a compatibilidade
    try:
        tipo_usuario = int(tipo_usuario)
    except (TypeError, ValueError):
        tipo_usuario = None

    if tipo_usuario == 1:
        return redirect(url_for('dashboard_admin'))      # Rota do Administrador
    elif tipo_usuario == 2:
        return redirect(url_for('painel_usuario'))    # Rota do Usuário Comum
    elif tipo_usuario == 3:
        return redirect(url_for('painel_servidor'))   # Rota do Servidor
    
    # Padrão de segurança caso venha algo inesperado
    return redirect(url_for('lista_usuarios'))


def logout():
    # Limpa todos os dados da sessão
    session.clear()
    return redirect(url_for('login'))