from flask import render_template, request, redirect, url_for
from models.sala import Sala
from models.instituicao import Instituicao

def nova_sala():
    if request.method == 'GET':
        instituicoes = Instituicao.listar_instituicoes_ativas()
        return render_template('admin/sala/nova.html', instituicoes=instituicoes)

    elif request.method == 'POST':
        telefone = request.form.get('telefone')
        andar = request.form.get('andar')
        numero = request.form.get('numero')
        descricao = request.form.get('descricao')
        predio = request.form.get('predio')
        instituicao_cnpj = request.form.get('instituicao_cnpj')
        laboratorio = bool(request.form.get('laboratorio'))
        sala_de_aula = bool(request.form.get('sala_de_aula'))

        instituicao = Instituicao.get_by_cnpj(instituicao_cnpj)
        if not instituicao:
            return "Instituição não encontrada", 404

        sala = Sala(
            telefone=telefone,
            andar=andar,
            numero=numero,
            descricao=descricao,
            predio=predio,
            instituicao=instituicao,
            laboratorio=laboratorio,
            sala_de_aula=sala_de_aula
        )

        if sala.save():
            return redirect(
                url_for('lista_salas')
            )

        return "Erro ao salvar sala", 500

    else:
        return "Método não permitido", 405
    
    
def lista_salas():
    salas = Sala.get_all()

    return render_template(
        'admin/sala/lista.html',
        salas=salas
    )