from functools import wraps
from flask import session, redirect, url_for, abort, render_template

def roles_required(*allowed_types):
    """
    Decorator para restringir o acesso a rotas com base nos tipos de usuário permitidos.
    Exemplo de uso: 
    @roles_required(1) -> Apenas Administrador
    @roles_required(1, 3) -> Administrador ou Servidor
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Verifica se o usuário está logado
            if 'usuario_username' not in session:
                return redirect(url_for('login'))
            
            # 2. Pega o tipo do usuário salvo na sessão
            user_type = session.get('usuario_tipo')
            
            # 3. Verifica se o tipo do usuário está na lista de permitidos
            if user_type not in allowed_types:
                # Retorna um erro 403 (Proibido) ou uma mensagem de acesso negado
                return render_template('admin/errors/403.html') if 'render_template' in globals() else ("Acesso negado: você não possui permissão para acessar esta página.", 403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator