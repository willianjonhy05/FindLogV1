from utils.email import validar_email
from utils.formata import formatar
from utils.cnpj import validar_cnpj


class Instituicao:


    def __init__(self, nome, cnpj, endereco, telefone, email):

        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.ativo = False



    def __str__(self):

        return self.nome



    def save(self):
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        resultado = dao.add_instituicao(self)
        return resultado == 1




    @staticmethod
    def get_all():
        from daos.instituicao_dao import InstituicaoDAO
        dao = InstituicaoDAO()
        return dao.get_instituicoes()





    # ==========================
    # NOME
    # ==========================

    @property
    def nome(self):

        return self._nome



    @nome.setter
    def nome(self, value):

        if not value or not value.strip():

            raise ValueError(
                "O nome da instituição não pode ser vazio."
            )

        self._nome = value.strip()





    # ==========================
    # CNPJ
    # ==========================

    @property
    def cnpj(self):

        return self._cnpj



    @cnpj.setter
    def cnpj(self, value):

        if not value or not validar_cnpj(value):

            raise ValueError(
                "O CNPJ informado não é válido."
            )

        self._cnpj = formatar(value)





    # ==========================
    # ENDEREÇO
    # ==========================

    @property
    def endereco(self):

        return self._endereco



    @endereco.setter
    def endereco(self, value):

        if not value or not value.strip():

            raise ValueError(
                "O endereço não pode ser vazio."
            )

        self._endereco = value.strip()





    # ==========================
    # TELEFONE
    # ==========================

    @property
    def telefone(self):

        return self._telefone



    @telefone.setter
    def telefone(self, value):

        if not value:

            raise ValueError(
                "O telefone não pode ser vazio."
            )


        value = formatar(value)


        if len(value) < 10:

            raise ValueError(
                "O telefone deve possuir pelo menos 11 dígitos."
            )


        self._telefone = value





    # ==========================
    # EMAIL
    # ==========================

    @property
    def email(self):

        return self._email



    @email.setter
    def email(self, value):

        if not value or not validar_email(value):

            raise ValueError(
                "O e-mail informado não é válido."
            )


        self._email = value





    # ==========================
    # STATUS
    # ==========================

    @property
    def ativo(self):

        return self._ativo



    @ativo.setter
    def ativo(self, value):

        if not isinstance(value, bool):

            raise ValueError(
                "O status deve ser booleano."
            )


        self._ativo = value