from flask import render_template, request
from models.instituicao import Instituicao
from models.categoria import Categoria
from models.usuario import Usuario
from models.sala import Sala
from models.item import Item
from flask import render_template_string



def index():
    return render_template('public/index.html')


def dashboard_admin():
    # Criação do dicionário com os dados
    context = {
        "total_instituicoes": Instituicao.quantidade(),
        "total_categorias": Categoria.contar_total(),
        "total_usuarios": Usuario.contar_total(),
        "total_salas": Sala.contar_total(),  # Incluído para a template não quebrar
        "total_itens": Item.contar_total()    # Incluído para a template não quebrar
    }
    
    # O operador ** desempacota o dicionário como variáveis nomeadas (kwarg)
    return render_template('admin/admin/dashboard.html', **context)

def visualizar_rotas():
    from main import app
    links = []
    for rule in app.url_map.iter_rules():
        # Filtra apenas métodos que aceitam GET para facilitar
        if "GET" in rule.methods:
            links.append({
                "endpoint": rule.endpoint,
                "methods": ', '.join(rule.methods),
                "url": str(rule)
            })
    
    # Template HTML simples integrado para exibir a lista
    html = """
    <div style="font-family: Arial, sans-serif; margin: 20px;">
        <h2>Rotas da Aplicação Flask</h2>
        <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%;">
            <tr style="background: #f2f2f2;">
                <th>Endpoint</th>
                <th>Métodos</th>
                <th>URL / Regra</th>
            </tr>
            {% for link in links %}
            <tr>
                <td>{{ link.endpoint }}</td>
                <td>{{ link.methods }}</td>
                <td><code>{{ link.url }}</code></td>
            </tr>
            {% endfor %}
        </table>
    </div>
    """
    return render_template_string(html, links=links)



# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     elif request.method == 'POST':
#         email = request.form.get("email")
#         senha = request.form.get("senha")
#         return "Login realizado com sucesso!"
#     else:
#         return "Método não permitido", 405
