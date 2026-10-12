from controller.main_controller import index, dashboard_admin
from controller.auth_controller import login, logout
from utils.auth import roles_required
from controller.main_controller import visualizar_rotas

def adicionar_rotas(app):
    app.add_url_rule('/', view_func=index, methods=['GET'])
    app.add_url_rule('/login', endpoint='login', view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', endpoint='logout', view_func=logout, methods=['GET'])
    app.add_url_rule('/dashboard', endpoint='dashboard_admin', view_func=roles_required(1)(dashboard_admin), methods=['GET'])
    app.add_url_rule('/admin/rotas', view_func=visualizar_rotas)