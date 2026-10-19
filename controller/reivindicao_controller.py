from models.reivindicacao import Reivindicacao
from flask import render_template 

def listar_revindicacoes():
    reivindicacoes = Reivindicacao.get_all()
    return render_template("admin/reivindicacao/lista.html", reivindicacoes=reivindicacoes)

def detalhar_reivindicacao(protocolo):
    reividicacao = Reivindicacao.pegar_por_protocolo(protocolo)
    if reividicacao:
        return render_template("admin/reivindicacao/detalhe.html", reividicacao=reividicacao)

    return render_template("admin/errors/404.html"), 404