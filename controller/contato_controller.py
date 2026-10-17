
from flask import render_template, request, redirect, url_for, flash
from models.contato import Contato


# Envio de mensagem pelo cliente
def nova_mensagem():
    if request.method == "POST":
        dados = {
            "nome": request.form.get("nome"),
            "email": request.form.get("email"),
            "telefone": request.form.get("telefone"),
            "assunto": request.form.get("assunto"),
            "mensagem": request.form.get("mensagem")
        }

        contato = Contato(data=dados)

        if contato.validate():
            contato.save()
            return redirect(url_for("index"))

        else:
            return render_template("admin/errors/404.html"), 404


# Lista de mensagens na área administrativa
def lista_contatos():
    contatos = Contato.get_all()

    return render_template(
        "admin/contato/lista.html",
        contatos=contatos
    )


# Visualiza uma mensagem específica
def contato_por_codigo(codigo):
    contato = Contato.get_by_codigo(codigo)

    if contato:
        return render_template(
            "admin/contato/detalhes.html",
            contato=contato
        )

    return render_template("admin/errors/404.html"), 404


# Apaga uma mensagem na área administrativa
def deletar_contato(codigo):
    contato = Contato.get_by_codigo(codigo)
    if contato:
        contato.delete()
        return redirect(url_for("lista_contatos"))
    return render_template("admin/errors/404.html"), 404
