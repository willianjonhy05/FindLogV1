
from controller.contato_controller import (
    enviar_mensagem,
    listar_contatos,
    novo_contato,
    detalhes_contato,
    atualizar_contato,
    deletar_contato
)


def registrar_rotas_contato(app):
    # Formulário público de contato
    app.add_url_rule(
        "/contato",
        view_func=enviar_mensagem,
        methods=["GET", "POST"],
        endpoint="contato"
    )

    # Cadastrar contato
    app.add_url_rule(
        "/contatos/novo",
        view_func=novo_contato,
        methods=["GET", "POST"],
        endpoint="novo_contato"
    )

    # Listar contatos
    app.add_url_rule(
        "/contatos/lista",
        view_func=listar_contatos,
        methods=["GET"],
        endpoint="lista_contatos"
    )

    # Detalhes de um contato
    app.add_url_rule(
        "/contatos/<int:id>/detalhes",
        view_func=detalhes_contato,
        methods=["GET"],
        endpoint="detalhes_contato"
    )

    # Atualizar contato
    app.add_url_rule(
        "/contatos/<int:id>/atualizar",
        view_func=atualizar_contato,
        methods=["GET", "POST"],
        endpoint="atualizar_contato"
    )

    # Excluir contato
    app.add_url_rule(
        "/contatos/<int:id>/deletar",
        view_func=deletar_contato,
        methods=["POST"],
        endpoint="deletar_contato"
    )
