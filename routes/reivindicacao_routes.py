from controller.reivindicao_controller import listar_revindicacoes, detalhar_reivindicacao
from utils.auth import roles_required

def reivindicacao_rotas(app):
    app.add_url_rule('/reivindicacoes', endpoint='lista_reivindicacoes', view_func=roles_required(1)(listar_revindicacoes), methods=['GET'])
    app.add_url_rule('/reivindicacoes/<protocolo>', endpoint='detalhar_reivindicacao', view_func=roles_required(1)(detalhar_reivindicacao), methods=['GET'])