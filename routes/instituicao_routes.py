
from controller.instituicao_controller import nova_instituicao, lista_instituicoes, deletar_instituicao, atualizar_instituicao, instituicao_por_cnpj

def instituicao_rotas(app):
    app.add_url_rule('/instituicao/nova', endpoint='nova_instituicao', view_func=nova_instituicao, methods=['GET', 'POST'])
    app.add_url_rule('/instituicao/lista', endpoint='lista_instituicoes', view_func=lista_instituicoes, methods=['GET'])
    app.add_url_rule('/instituicao/deletar/<cnpj>', endpoint='deletar_instituicao', view_func=deletar_instituicao, methods=['POST'])
    app.add_url_rule('/instituicao/detalhes/<cnpj>', endpoint='view_instituicao', view_func=instituicao_por_cnpj, methods=['GET'])
    app.add_url_rule('/instituicao/atualizar/<cnpj>', endpoint='atualizar_instituicao', view_func=atualizar_instituicao, methods=['GET', 'POST'])
    