from utils.email import validar_email
from utils.formata import formatar
from utils.cnpj import validar_cnpj


class Instituicao:
    def __init__(self, data):
        self.data = data
        self.errors = []

        if "ativo" not in self.data:
            self.data["ativo"] = False

    def __str__(self):
        return self.data.get("nome", "Nome não definido")
    
    def validate(self):
        self.errors = []
        if not self.data.get("nome") or not self.data.get("nome").strip():
            self.errors.append("O nome da instituição não pode ser vazio.")

        # Validação do CNPJ
        cnpj = self.data.get("cnpj")
        if not cnpj:
            self.errors.append("O CNPJ não pode ser vazio.")
        else:
            cnpj_valido = validar_cnpj(cnpj)
            if isinstance(cnpj_valido, str):
                self.errors.append(cnpj_valido)

        # Validação do endereço
        if not self.data.get("endereco") or not self.data.get("endereco").strip():
            self.errors.append("O endereço não pode ser vazio.")

        # Validação do telefone
        telefone = self.data.get("telefone")
        if not telefone:
            self.errors.append("O telefone não pode ser vazio.")
        else:
            telefone_formatado = formatar(telefone)
            if len(telefone_formatado) < 10:
                self.errors.append("O telefone deve possuir pelo menos 10 dígitos.")

        # Validação do e-mail
        email = self.data.get("email")
        if not email:
            self.errors.append("O e-mail não pode ser vazio.")
        else:
            email_valido = validar_email(email)
            if isinstance(email_valido, str):
                self.errors.append(email_valido)

        return len(self.errors) == 0

    def save(self):
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        return dao.add_instituicao(self)
    
    def delete(self):
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        dao.deletar_instituicao(self.cnpj)
         
    def update(self):
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        dao.atualizar_instituicao(self)

    @staticmethod
    def quantidade():
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO
        return dao.quantidade_instituicoes()
    
    # def __init__(self, nome, cnpj, endereco, telefone, email):
    #     self.nome = nome
    #     self.cnpj = cnpj
    #     self.endereco = endereco
    #     self.telefone = telefone
    #     self.email = email
    #     self.ativo = False

        # self.data = data
        # self.errors = []

    # def validate():
    #     pass

    @staticmethod
    def listar_instituicoes_ativas():
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        return dao.get_nome_e_cnpj_ativos()
    
    @staticmethod
    def nome_por_cnpj(cnpj):
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        return dao.get_nome_por_cnpj(cnpj)

    @staticmethod
    def get_all():
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        return dao.get_instituicoes()

    @staticmethod
    def get_paginated(page=1, per_page=10, search=None):
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        return dao.get_instituicoes_paginated(page=page, per_page=per_page, search=search)
    
    @staticmethod
    def get_by_cnpj(cnpj):
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        return dao.get_instituicao_by_cnpj(cnpj)    

    @property
    def nome(self):
        return self.data.get("nome")

    @property
    def cnpj(self):
        return self.data.get("cnpj")

    @property
    def endereco(self):
        return self.data.get("endereco")

    @property
    def telefone(self):
        return self.data.get("telefone")

    @property
    def email(self):
        return self.data.get("email")

    @property
    def ativo(self):
        return self.data.get("ativo", False)

    @ativo.setter
    def ativo(self, value):
        if not isinstance(value, bool):
            raise ValueError("O status deve ser booleano.")
        self.data["ativo"] = value