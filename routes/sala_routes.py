
from controller.sala_controller import nova_sala, lista_salas

def sala_rotas(app):
    app.add_url_rule('/sala/nova', endpoint='nova_sala', view_func=nova_sala, methods=['GET', 'POST'])
    app.add_url_rule('/sala/lista', endpoint='lista_salas', view_func=lista_salas, methods=['GET'])
