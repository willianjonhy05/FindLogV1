from models.instituicao import Instituicao
from utils.formata import formatar
from utils.email import validar_email

class Sala:
    def __init__(self, data=None):
        self.data = data or {}
        self.errors = []

        # Valores booleanos padrão
        if "laboratorio" not in self.data:
            self.data["laboratorio"] = False

        if "sala_de_aula" not in self.data:
            self.data["sala_de_aula"] = False

        # Gera o código inicial caso os dados necessários estejam presentes e o código não exista
        if not self.data.get("codigo"):
            predio = self.data.get("predio")
            numero = self.data.get("numero")
            andar = self.data.get("andar")
            if predio and numero and andar:
                self.data["codigo"] = self._gerar_codigo_da_sala(predio, numero, andar)

    def __str__(self):
        return f"Sala {self.numero} - Prédio {self.predio}"

    def validate(self, is_new=True):
        self.errors = []  # Limpa a lista de erros antes de validar

        # Prédio (Obrigatório)
        predio = self.data.get("predio")
        if not predio or not str(predio).strip():
            self.errors.append("O prédio da sala não pode ser vazio.")

        # Número (Obrigatório)
        numero = self.data.get("numero")
        if not numero or not str(numero).strip():
            self.errors.append("O número da sala não pode ser vazio.")

        # Andar (Obrigatório)
        andar = self.data.get("andar")
        if not andar or not str(andar).strip():
            self.errors.append("O andar da sala não pode ser vazio.")

        # Descrição (Obrigatório)
        descricao = self.data.get("descricao")
        if not descricao or not str(descricao).strip():
            self.errors.append("A descrição da sala não pode ser vazia.")

        # Instituição (Obrigatório e deve existir)
        codigo_instituicao = self.data.get("instituicao")
        if not codigo_instituicao:
            self.errors.append("A instituição da sala não pode ser vazia.")
        else:
            instituicao = Instituicao.get_by_cnpj(codigo_instituicao)
            if not instituicao:
                self.errors.append("A instituição associada à sala não existe.")

        # Telefone (Opcional)
        telefone = self.data.get("telefone")
        if telefone and str(telefone).strip():
            telefone_formatado = formatar(str(telefone))
            if len(telefone_formatado) < 10:
                self.errors.append("O telefone deve possuir pelo menos 10 dígitos.")

        # E-mail (Opcional)
        email = self.data.get("email")
        if email and str(email).strip():
            email_valido = validar_email(email)
            if isinstance(email_valido, str):
                self.errors.append(email_valido)

        # Unicidade do Código (Apenas para novos cadastros)
        if is_new and predio and numero and andar:
            codigo = self._gerar_codigo_da_sala(predio, numero, andar)
            if Sala.get_by_codigo(codigo):
                self.errors.append("Já existe uma sala cadastrada com esta combinação de Prédio, Número e Andar.")

        return len(self.errors) == 0

    @classmethod
    def _gerar_codigo_da_sala(cls, predio, numero, andar):
        """Gera um código único para a sala com base no prédio, número e andar"""
        primeira_letra_predio = str(predio).strip()[0].upper()
        return f"{primeira_letra_predio}{str(numero).strip()}{str(andar).strip()}"

    def save(self):
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        return dao.add_sala(self)

    def update(self):
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        return dao.atualizar_sala(self)

    def delete(self):
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        return dao.deletar_sala(self.codigo)

    @staticmethod
    def contar_total():
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        return dao.contar_total()

    @staticmethod
    def get_all():
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        return dao.get_salas()

    @staticmethod
    def get_all_by_cnpj(cnpj):
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        return dao.get_salas_por_cnpj(cnpj)

    @staticmethod
    def get_by_codigo(codigo):
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        return dao.get_sala_by_codigo(codigo)

    # ==========================
    # PROPRIEDADES (Getters e Setters)
    # ==========================

    @property
    def codigo(self):
        return self.data.get("codigo")

    @property
    def predio(self):
        return self.data.get("predio")

    @predio.setter
    def predio(self, value):
        if not value or not str(value).strip():
            raise ValueError("O prédio da sala não pode ser vazio.")
        self.data["predio"] = str(value).strip()

    @property
    def numero(self):
        return self.data.get("numero")

    @numero.setter
    def numero(self, value):
        if not value or not str(value).strip():
            raise ValueError("O número da sala não pode ser vazio.")
        self.data["numero"] = str(value).strip()

    @property
    def andar(self):
        return self.data.get("andar")

    @andar.setter
    def andar(self, value):
        if not value or not str(value).strip():
            raise ValueError("O andar da sala não pode ser vazio.")
        self.data["andar"] = str(value).strip()

    @property
    def instituicao(self):
        return self.data.get("instituicao")

    @instituicao.setter
    def instituicao(self, value):
        if not value:
            raise ValueError("A instituição da sala não pode ser vazia.")
        self.data["instituicao"] = value

    @property
    def descricao(self):
        return self.data.get("descricao")

    @descricao.setter
    def descricao(self, value):
        if not value or not str(value).strip():
            raise ValueError("A descrição da sala não pode ser vazia.")
        self.data["descricao"] = str(value).strip()

    @property
    def telefone(self):
        return self.data.get("telefone")

    @telefone.setter
    def telefone(self, value):
        if value and str(value).strip():
            formatado = formatar(str(value))
            if len(formatado) < 10:
                raise ValueError("O telefone deve possuir pelo menos 10 dígitos.")
            self.data["telefone"] = formatado
        else:
            self.data["telefone"] = None

    @property
    def email(self):
        return self.data.get("email")

    @email.setter
    def email(self, value):
        if value and str(value).strip():
            valido = validar_email(value)
            if isinstance(valido, str):
                raise ValueError(valido)
            self.data["email"] = value.strip()
        else:
            self.data["email"] = None

    @property
    def laboratorio(self):
        return self.data.get("laboratorio", False)

    @laboratorio.setter
    def laboratorio(self, value):
        if not isinstance(value, bool):
            raise ValueError("O campo 'laboratorio' deve ser um valor booleano.")
        self.data["laboratorio"] = value

    @property
    def sala_de_aula(self):
        return self.data.get("sala_de_aula", False)

    @sala_de_aula.setter
    def sala_de_aula(self, value):
        if not isinstance(value, bool):
            raise ValueError("O campo 'sala_de_aula' deve ser um valor booleano.")
        self.data["sala_de_aula"] = value