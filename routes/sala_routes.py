
from controller.sala_controller import nova_sala, lista_salas, editar_sala, deletar_sala, detalhes_sala

def sala_rotas(app):
    app.add_url_rule('/sala/nova', endpoint='nova_sala', view_func=nova_sala, methods=['GET', 'POST'])
    app.add_url_rule('/sala/lista', endpoint='lista_salas', view_func=lista_salas, methods=['GET'])
    app.add_url_rule('/sala/editar/<codigo>', endpoint='editar_sala', view_func=editar_sala, methods=['GET', 'POST'])
    app.add_url_rule('/sala/deletar/<codigo>', endpoint='deletar_sala', view_func=deletar_sala, methods=['POST'])
    app.add_url_rule('/sala/<codigo>', endpoint='detalhes_sala', view_func=detalhes_sala, methods=['GET'])
