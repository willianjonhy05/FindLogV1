from flask import render_template, request, redirect, url_for
from models.instituicao import Instituicao


def nova_instituicao():
    if request.method == 'GET':
        return render_template('admin/instituicao/nova.html')

    elif request.method == 'POST':
        # Recolhe os dados enviados pelo formulário em um dicionário
        dados = {
            "cnpj": request.form.get('cnpj'),
            "nome": request.form.get('nome'),
            "endereco": request.form.get('endereco'),
            "telefone": request.form.get('telefone'),
            "email": request.form.get('email'),
            "ativo": True # Padrão para nova instituição
        }

        # Instancia a classe passando o dicionário data
        instituicao = Instituicao(data=dados)

        # Valida os dados antes de salvar
        if instituicao.validate():
            instituicao.save()
            return redirect(url_for('lista_instituicoes'))
        
        # Se houver erros, podemos reenderizar o template passando a instituição e os erros 
        # (caso sua template exiba self.errors, ela funcionará sem alteração)
        return render_template(
            'admin/instituicao/nova.html',
            instituicao=instituicao,
            erros=instituicao.errors
        ), 400

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
    return "Instituição não encontrada", 404
    
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
        # Atualiza os dados dentro do dicionário interno da instituição
        instituicao.data['nome'] = request.form.get('nome')
        instituicao.data['endereco'] = request.form.get('endereco')
        instituicao.data['telefone'] = request.form.get('telefone')
        instituicao.data['email'] = request.form.get('email')
        instituicao.ativo = request.form.get('ativo') == "1" or request.form.get('ativo') == "on"

        # Valida as alterações antes de persistir
        if instituicao.validate():
            instituicao.update()
            return redirect(url_for('lista_instituicoes'))

        # Se falhar na validação, retorna para a tela de atualização com os erros
        return render_template(
            'admin/instituicao/atualizar.html',
            instituicao=instituicao,
            erros=instituicao.errors
        ), 400

    else:
        return "Método não permitido", 405
    
def instituicao_por_cnpj(cnpj):
    from models.usuario import Usuario
    instituicao = Instituicao.get_by_cnpj(cnpj)
    qtde_usuarios = Usuario.quantidade_de_usuarios_por_instituicao(cnpj)
    usuarios = Usuario.get_all_by_instituicao(cnpj)

    context = {
        "instituicao": instituicao,
        "qtde_usuarios": qtde_usuarios,
        "usuarios": usuarios
    }

    if instituicao:
        return render_template(
            'admin/instituicao/detalhes.html',
            **context
        )
    else:
        return "Instituição não encontrada", 404