from controller import main_controller

def adicionar_rotas(app):
    app.add_url_rule('/', view_func=main_controller.index, methods=['GET'])