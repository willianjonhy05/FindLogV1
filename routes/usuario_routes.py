
from controller.usuario_controller import novo_usuario, lista_usuarios, deletar_usuario, visualizar_usuario, editar_usuario
from utils.auth import roles_required

def usuario_routes(app):
    app.add_url_rule('/usuario/novo', endpoint='novo_usuario', view_func=novo_usuario, methods=['GET', 'POST'])
    app.add_url_rule('/usuario/lista', endpoint='lista_usuarios', view_func=roles_required(1)(lista_usuarios), methods=['GET'])
    app.add_url_rule('/usuario/editar/<username>', endpoint='editar_usuario', view_func=roles_required(1)(editar_usuario), methods=['GET', 'POST'])
    app.add_url_rule('/usuario/deletar/<username>', endpoint='deletar_usuario', view_func=roles_required(1)(deletar_usuario), methods=['POST'])
    app.add_url_rule('/usuario/<username>', endpoint='visualizar_usuario', view_func=roles_required(1)(visualizar_usuario), methods=['GET'])