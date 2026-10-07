from flask import render_template, request, redirect, url_for
from models.sala import Sala
from models.instituicao import Instituicao

def nova_sala():
    if request.method == 'GET':
        instituicoes = Instituicao.listar_instituicoes_ativas()
        return render_template('admin/sala/nova.html', instituicoes=instituicoes)

    elif request.method == 'POST':
        # Empacota os dados do formulário em um dicionário compatível com a classe Sala
        dados = {
            "telefone": request.form.get('telefone'),
            "andar": request.form.get('andar'),
            "numero": request.form.get('numero'),
            "descricao": request.form.get('descricao'),
            "predio": request.form.get('predio'),
            "instituicao": request.form.get('instituicao_cnpj'),
            "laboratorio": True if request.form.get('laboratorio') else False,
            "sala_de_aula": True if request.form.get('sala_de_aula') else False
        }

        # Instancia a classe passando o dicionário data
        sala = Sala(data=dados)

        # Valida os dados (is_new=True verifica unicidade do código gerado)
        if sala.validate(is_new=True):
            if sala.save():
                return redirect(url_for('lista_salas'))
            return "Erro ao salvar sala no banco de dados", 500

        # Se falhar na validação, retorna para o template com os erros e as instituições
        instituicoes = Instituicao.listar_instituicoes_ativas()
        return render_template(
            'admin/sala/nova.html',
            sala=sala,
            instituicoes=instituicoes,
            erros=sala.errors
        ), 400

    else:
        return "Método não permitido", 405
    
def lista_salas():
    salas = Sala.get_all()
    return render_template(
        'admin/sala/lista.html',
        salas=salas
    )

def editar_sala(codigo):
    sala = Sala.get_by_codigo(codigo)
    if not sala:
        return "Sala não encontrada", 404

    if request.method == 'GET':
        instituicoes = Instituicao.listar_instituicoes_ativas()
        return render_template(
            'admin/sala/editar.html',
            sala=sala,
            instituicoes=instituicoes
        )

    elif request.method == 'POST':
        # Atualiza os dados através das propriedades para disparar os setters internos
        try:
            sala.telefone = request.form.get('telefone')
            sala.andar = request.form.get('andar')
            sala.numero = request.form.get('numero')
            sala.descricao = request.form.get('descricao')
            sala.predio = request.form.get('predio')
            sala.instituicao = request.form.get('instituicao_cnpj')
            sala.laboratorio = True if request.form.get('laboratorio') else False
            sala.sala_de_aula = True if request.form.get('sala_de_aula') else False
        except ValueError as e:
            instituicoes = Instituicao.listar_instituicoes_ativas()
            return render_template(
                'admin/sala/editar.html',
                sala=sala,
                instituicoes=instituicoes,
                erros=[str(e)]
            ), 400

        # Valida a atualização (is_new=False pois a sala já existe)
        if sala.validate(is_new=False):
            if sala.update():
                return redirect(url_for('lista_salas'))
            return "Erro ao atualizar sala no banco de dados", 500

        # Se houver erros de validação
        instituicoes = Instituicao.listar_instituicoes_ativas()
        return render_template(
            'admin/sala/editar.html',
            sala=sala,
            instituicoes=instituicoes,
            erros=sala.errors
        ), 400

    else:
        return "Método não permitido", 405
    
def deletar_sala(codigo):
    sala = Sala.get_by_codigo(codigo)
    if not sala:
        return "Sala não encontrada", 404

    if request.method == 'POST':
        if sala.delete():
            return redirect(url_for('lista_salas'))
        return "Erro ao deletar sala", 500

    else:
        return "Método não permitido", 405
    

def detalhes_sala(codigo):
    sala = Sala.get_by_codigo(codigo)
    if not sala:
        return "Sala não encontrada", 404

    return render_template(
        'admin/sala/detalhes.html',
        sala=sala
    )