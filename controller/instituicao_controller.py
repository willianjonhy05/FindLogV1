from flask import render_template, request, redirect, url_for
from models.instituicao import Instituicao



def nova_instituicao():
    if request.method == 'GET':
        return render_template('admin/instituicao/nova.html')

    elif request.method == 'POST':
        cnpj = request.form.get('cnpj')
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        instituicao = Instituicao(
            nome=nome,
            cnpj=cnpj,
            endereco=endereco,
            telefone=telefone,
            email=email
        )
        instituicao.ativo = True

        if instituicao.save():
            return redirect(
                url_for('lista_instituicoes')
            )

        return "Erro ao salvar instituição", 500

    else:

        return "Método não permitido", 405




def lista_instituicoes():

    instituicoes = Instituicao.get_all()


    return render_template(
        'admin/instituicao/lista.html',
        instituicoes=instituicoes
    )