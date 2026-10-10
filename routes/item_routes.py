
from controller.item_controller import novo_item, lista_itens, editar_item, deletar_item, visualizar_item

def item_rotas(app):
    app.add_url_rule('/item/novo', endpoint='novo_item', view_func=novo_item, methods=['GET', 'POST'])
    app.add_url_rule('/item/lista', endpoint='lista_items', view_func=lista_itens, methods=['GET'])
    app.add_url_rule('/item/editar/<codigo>', endpoint='editar_item', view_func=editar_item, methods=['GET', 'POST'])
    app.add_url_rule('/item/deletar/<codigo>', endpoint='deletar_item', view_func=deletar_item, methods=['POST'])
    app.add_url_rule('/item/<codigo>', endpoint='visualizar_item', view_func=visualizar_item, methods=['GET'])
