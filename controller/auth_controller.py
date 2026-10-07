from flask import render_template, request, redirect, url_for, session
from models.usuario import Usuario

def login():
    if request.method == 'GET':
        # Se já estiver logado, redireciona para a home/dashboard
        if 'usuario_username' in session:
            return redirect(url_for('lista_usuarios'))
        return render_template('login.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')

        if not username or not senha:
            return render_template('login.html', erro="Preencha todos os campos."), 400

        # Busca o usuário pelo username
        usuario = Usuario.get_by_username(username)

        # Valida se o usuário existe, está ativo e se a senha está correta
        if usuario and usuario.ativo and usuario.verificar_senha(senha):
            # Salva os dados essenciais na sessão do Flask
            session['usuario_username'] = usuario.username
            session['usuario_nome'] = usuario.nome
            session['usuario_tipo'] = usuario.tipo_usuario
            
            return redirect(url_for('lista_usuarios')) # Altere para sua rota inicial protegida

        return render_template('login.html', erro="Usuário ou senha inválidos."), 401

    else:
        return "Método não permitido", 405


def logout():
    # Limpa todos os dados da sessão
    session.clear()
    return redirect(url_for('login'))