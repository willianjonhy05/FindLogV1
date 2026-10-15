
from flask import render_template, request, redirect, url_for, flash

from models.contato import Contato
from daos.contato_dao import ContatoDAO


def enviar_mensagem():
    if request.method == "GET":
        return redirect(url_for("index", _anchor="contato"))

    try:
        contato = _criar_contato()
        resultado = ContatoDAO().inserir(contato)

        if resultado:
            flash("Mensagem enviada com sucesso!", "success")
        else:
            flash(
                "Não foi possível confirmar o salvamento da mensagem.",
                "warning"
            )

        return redirect(url_for("index", _anchor="contato"))

    except ValueError as erro:
        flash(str(erro), "danger")

    except Exception as erro:
        print("ERRO AO SALVAR CONTATO:", repr(erro))
        flash("Erro ao enviar a mensagem. Tente novamente.", "danger")

    return render_template("public/index.html"), 400


def novo_contato():
    if request.method == "POST":
        try:
            contato = _criar_contato()
            resultado = ContatoDAO().inserir(contato)

            if resultado:
                flash("Contato cadastrado com sucesso!", "success")
                return redirect(url_for("lista_contatos"))

            flash("Não foi possível cadastrar o contato.", "danger")

        except ValueError as erro:
            flash(str(erro), "danger")

        except Exception:
            flash("Ocorreu um erro ao cadastrar o contato.", "danger")

    return render_template("admin/contato/nova.html")


def listar_contatos():
    try:
        contatos = ContatoDAO().listar_todos()
        return render_template(
            "admin/contato/lista.html",
            contatos=contatos
        )
    except Exception:
        flash("Não foi possível carregar os contatos.", "danger")
        return render_template(
            "admin/contato/lista.html",
            contatos=[]
        )


def detalhes_contato(id):
    contato = ContatoDAO().buscar_por_id(id)

    if not contato:
        return render_template("admin/errors/404.html"), 404

    return render_template(
        "admin/contato/detalhes.html",
        contato=contato
    )


def atualizar_contato(id):
    dao = ContatoDAO()
    contato_atual = dao.buscar_por_id(id)

    if not contato_atual:
        return render_template("admin/errors/404.html"), 404

    if request.method == "POST":
        try:
            contato = _criar_contato()
            resultado = dao.atualizar(id, contato)

            if resultado:
                flash("Contato atualizado com sucesso!", "success")
                return redirect(url_for("detalhes_contato", id=id))

            flash("Não foi possível atualizar o contato.", "danger")

        except ValueError as erro:
            flash(str(erro), "danger")

        except Exception:
            flash("Ocorreu um erro ao atualizar o contato.", "danger")

    return render_template(
        "admin/contato/atualizar.html",
        contato=contato_atual
    )


def deletar_contato(id):
    if request.method != "POST":
        return render_template("admin/errors/405.html"), 405

    try:
        dao = ContatoDAO()
        contato = dao.buscar_por_id(id)

        if not contato:
            return render_template("admin/errors/404.html"), 404

        resultado = dao.deletar(id)

        if resultado:
            flash("Contato excluído com sucesso!", "success")
        else:
            flash("Não foi possível excluir o contato.", "danger")

    except Exception:
        flash("Ocorreu um erro ao excluir o contato.", "danger")

    return redirect(url_for("lista_contatos"))


def _criar_contato():
    return Contato(
        nome=request.form.get("nome", "").strip(),
        email=request.form.get("email", "").strip(),
        telefone=request.form.get("telefone", "").strip(),
        assunto=request.form.get("assunto", "").strip(),
        mensagem=request.form.get("mensagem", "").strip()
    )
