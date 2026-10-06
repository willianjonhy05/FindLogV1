from controller.categoria_controller import nova_categoria, listar_categorias, atualizar_categoria, apagar_categoria, visualizar_categoria


def categoria_routes(app):
    app.add_url_rule('/categoria/nova', endpoint='nova_categoria', view_func=nova_categoria, methods=['GET', 'POST'])
    app.add_url_rule('/categoria/lista', endpoint='lista_categorias', view_func=listar_categorias, methods=['GET'])
    app.add_url_rule('/categoria/deletar/<codigo>', endpoint='deletar_categoria', view_func=apagar_categoria, methods=['POST'])
    app.add_url_rule('/categoria/detalhes/<codigo>', endpoint='view_categoria', view_func=visualizar_categoria, methods=['GET'])
    app.add_url_rule('/categoria/atualizar/<codigo>', endpoint='atualizar_categoria', view_func=atualizar_categoria, methods=['GET', 'POST'])
