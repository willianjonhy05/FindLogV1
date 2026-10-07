from controller import main_controller
from controller.auth_controller import login, logout

def adicionar_rotas(app):
    app.add_url_rule('/', view_func=main_controller.index, methods=['GET'])
    app.add_url_rule('/login', endpoint='login', view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', endpoint='logout', view_func=logout, methods=['GET'])