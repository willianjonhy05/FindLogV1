from utils.auth import roles_required
from controller.item_controller import novo_item, lista_itens, editar_item, deletar_item, visualizar_item

def item_rotas(app):
    app.add_url_rule('/item/novo', endpoint='novo_item', view_func=roles_required(1)(novo_item), methods=['GET', 'POST'])
    app.add_url_rule('/item/lista', endpoint='lista_items', view_func=roles_required(1)(lista_itens), methods=['GET'])
    app.add_url_rule('/item/editar/<codigo>', endpoint='editar_item', view_func=roles_required(1)(editar_item), methods=['GET', 'POST'])
    app.add_url_rule('/item/deletar/<codigo>', endpoint='deletar_item', view_func=roles_required(1)(deletar_item), methods=['POST'])
    app.add_url_rule('/item/<codigo>', endpoint='visualizar_item', view_func=roles_required(1)(visualizar_item), methods=['GET'])
