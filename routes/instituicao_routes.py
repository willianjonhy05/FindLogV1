#from utils.auth import roles_required
from controller.instituicao_controller import nova_instituicao, lista_instituicoes, deletar_instituicao, atualizar_instituicao, instituicao_por_cnpj

def instituicao_rotas(app):
    app.add_url_rule('/instituicao/nova', endpoint='nova_instituicao', view_func=nova_instituicao, methods=['GET', 'POST'])
    app.add_url_rule('/instituicao/lista', endpoint='lista_instituicoes', view_func=lista_instituicoes, methods=['GET'])
    app.add_url_rule('/instituicao/deletar/<cnpj>', endpoint='deletar_instituicao', view_func=deletar_instituicao, methods=['POST'])
    app.add_url_rule('/instituicao/detalhes/<cnpj>', endpoint='view_instituicao', view_func=instituicao_por_cnpj, methods=['GET'])
    app.add_url_rule('/instituicao/atualizar/<cnpj>', endpoint='atualizar_instituicao', view_func=atualizar_instituicao, methods=['GET', 'POST'])


    # 1. Apenas Administradores (Tipo 1) podem gerenciar usuários
    # app.add_url_rule('/admin/usuarios', 'lista_usuarios', roles_required(1)(lista_usuarios), methods=['GET'])
    # app.add_url_rule('/admin/usuarios/novo', 'novo_usuario', roles_required(1)(nova_usuario), methods=['GET', 'POST'])

    # # 2. Administradores (1) e Servidores (3) podem cadastrar salas
    # app.add_url_rule('/admin/salas/nova', 'nova_sala', roles_required(1, 3)(nova_sala), methods=['GET', 'POST'])

    # # 3. Qualquer usuário logado (1, 2 ou 3) pode acessar uma rota comum
    # # (Caso queira permitir todos os logados, basta passar todos os tipos)
    # app.add_url_rule('/dashboard', 'dashboard', roles_required(1, 2, 3)(dashboard_view), methods=['GET'])    