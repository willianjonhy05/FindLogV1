
from controller.contato_controller import (
    nova_mensagem,
    lista_contatos,
    contato_por_codigo,
    deletar_contato
)


def registrar_rotas_contato(app):
    # Envio de mensagem pelo formulário público
    app.add_url_rule(
        "/contato",
        view_func=nova_mensagem,
        methods=["POST", "GET"],
        endpoint="contato"
    )

    # Listar mensagens na área administrativa
    app.add_url_rule(
        "/contatos/listar",
        view_func=lista_contatos,
        methods=["GET"],
        endpoint="lista_contatos"
    )

    # Visualizar uma mensagem específica
    app.add_url_rule(
        "/contatos/<string:codigo>",
        view_func=contato_por_codigo,
        methods=["GET"],
        endpoint="contato_por_codigo"
    )

    # Excluir uma mensagem na área administrativa
    app.add_url_rule(
        "/contatos/<string:codigo>/deletar",
        view_func=deletar_contato,
        methods=["POST"],
        endpoint="deletar_contato"
    )
