
from controller.instituicao import views

def instituicao_rotas(app):
    app.add_url_rule('/instituicao/nova', endpoint='nova_instituicao', view_func=views.nova_instituicao, methods=['GET', 'POST'])
    app.add_url_rule('/instituicao/lista', endpoint='lista_instituicoes', view_func=views.lista_instituicoes, methods=['GET'])