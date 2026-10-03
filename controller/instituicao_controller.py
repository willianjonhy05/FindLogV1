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
    
    
def deletar_instituicao(cnpj):
    instituicao = Instituicao.get_by_cnpj(cnpj)
    if instituicao:
        instituicao.delete()
        return redirect(url_for('lista_instituicoes'))
    
def atualizar_instituicao(cnpj):
    instituicao = Instituicao.get_by_cnpj(cnpj)
    if not instituicao:
        return "Instituição não encontrada", 404

    if request.method == 'GET':
        return render_template(
            'admin/instituicao/atualizar.html',
            instituicao=instituicao
        )

    elif request.method == 'POST':
        instituicao.nome = request.form.get('nome')
        instituicao.endereco = request.form.get('endereco')
        instituicao.telefone = request.form.get('telefone')
        instituicao.email = request.form.get('email')
        instituicao.ativo = bool(request.form.get('ativo'))

        instituicao.update()
        return redirect(url_for('lista_instituicoes'))

    else:
        return "Método não permitido", 405
    
def instituicao_por_cnpj(cnpj):
    instituicao = Instituicao.get_by_cnpj(cnpj)
    if instituicao:
        return render_template(
            'admin/instituicao/detalhes.html',
            instituicao=instituicao
        )
    else:
        return "Instituição não encontrada", 404