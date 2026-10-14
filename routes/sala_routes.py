from utils.auth import roles_required
from controller.sala_controller import nova_sala, lista_salas, editar_sala, deletar_sala, detalhes_sala

def sala_rotas(app):
    app.add_url_rule('/sala/nova', endpoint='nova_sala', view_func=roles_required(1)(nova_sala), methods=['GET', 'POST'])
    app.add_url_rule('/sala/lista', endpoint='lista_salas', view_func=roles_required(1)(lista_salas), methods=['GET'])
    app.add_url_rule('/sala/editar/<codigo>', endpoint='editar_sala', view_func=roles_required(1)(editar_sala), methods=['GET', 'POST'])
    app.add_url_rule('/sala/deletar/<codigo>', endpoint='deletar_sala', view_func=roles_required(1)(deletar_sala), methods=['POST'])
    app.add_url_rule('/sala/<codigo>', endpoint='detalhes_sala', view_func=roles_required(1)(detalhes_sala), methods=['GET'])
