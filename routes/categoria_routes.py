from controller.categoria_controller import nova_categoria, listar_categorias, atualizar_categoria, apagar_categoria, visualizar_categoria
from utils.auth import roles_required

def categoria_routes(app):
    app.add_url_rule('/categoria/nova', endpoint='nova_categoria', view_func=roles_required(1)(nova_categoria), methods=['GET', 'POST'])
    app.add_url_rule('/categoria/lista', endpoint='lista_categorias', view_func=roles_required(1)(listar_categorias), methods=['GET'])
    app.add_url_rule('/categoria/deletar/<codigo>', endpoint='deletar_categoria', view_func=roles_required(1)(apagar_categoria), methods=['POST'])
    app.add_url_rule('/categoria/detalhes/<codigo>', endpoint='view_categoria', view_func=roles_required(1)(visualizar_categoria), methods=['GET'])
    app.add_url_rule('/categoria/atualizar/<codigo>', endpoint='atualizar_categoria', view_func=roles_required(1)(atualizar_categoria), methods=['GET', 'POST'])
