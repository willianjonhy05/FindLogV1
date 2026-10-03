
from controller.instituicao_controller import nova_instituicao, lista_instituicoes

def instituicao_rotas(app):
    app.add_url_rule('/instituicao/nova', endpoint='nova_instituicao', view_func=nova_instituicao, methods=['GET', 'POST'])
    app.add_url_rule('/instituicao/lista', endpoint='lista_instituicoes', view_func=lista_instituicoes, methods=['GET'])