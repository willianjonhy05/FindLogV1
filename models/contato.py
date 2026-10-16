from datetime import datetime

from utils.formata import formatar
from utils.email import validar_email
from utils.codigo import gerar_codigo


class Contato:
    ASSUNTOS = {
        1: "Dúvidas e orientações",
        2: "Sugestões de melhorias",
        3: "Reclamações",
        4: "Problemas técnicos",
        5: "Outro assunto"
    }

    def __init__(self, data):
        self.data = data
        self.errors = []

        # Data de envio
        if not self.data.get("data_envio"):
            self.data["data_envio"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        # Código único para o contato
        if not self.data.get("codigo"):
            while True:
                codigo = gerar_codigo()

                if not Contato.contato_by_codigo(codigo):
                    self.data["codigo"] = codigo
                    break

    def __str__(self):
        return self.nome or "Contato sem nome"

    def validate(self, is_new=True):
        self.errors = []

        # Validação do nome
        nome = self.data.get("nome")
        if not nome or not str(nome).strip():
            self.errors.append("O nome não pode ser vazio.")
        elif len(str(nome).strip()) > 100:
            self.errors.append("O nome deve ter no máximo 100 caracteres.")

        # Validação do telefone
        telefone = self.data.get("telefone")
        if not telefone or not str(telefone).strip():
            self.errors.append("O telefone não pode ser vazio.")
        else:
            telefone_formatado = formatar(telefone)
            if len(telefone_formatado) < 10:
                self.errors.append(
                    "O telefone deve possuir pelo menos 10 dígitos."
                )
            if len(str(telefone).strip()) > 20:
                self.errors.append(
                    "O telefone deve ter no máximo 20 caracteres."
                )

        # Validação do e-mail
        email = self.data.get("email")
        if not email or not str(email).strip():
            self.errors.append("O e-mail não pode ser vazio.")
        else:
            email_valido = validar_email(email)
            if isinstance(email_valido, str):
                self.errors.append(email_valido)


        # Validação do assunto
        assunto = self.data.get("assunto")

        if assunto is None or not str(assunto).strip():
            self.errors.append("O assunto não pode ser vazio.")
        else:
            assunto = str(assunto).strip()

            assuntos_validos = {
                str(codigo) for codigo in self.ASSUNTOS
            } | set(self.ASSUNTOS.values())

            if assunto not in assuntos_validos:
                self.errors.append(
                    "Selecione um assunto válido dentre as opções disponíveis."
                )
            else:
                # Se foi enviado o código numérico, converte para o texto.
                for codigo, descricao in self.ASSUNTOS.items():
                    if assunto == str(codigo):
                        self.data["assunto"] = descricao
                        break


        # Validação da mensagem
        mensagem = self.data.get("mensagem")
        if not mensagem or not str(mensagem).strip():
            self.errors.append("A mensagem não pode ser vazia.")
        elif len(str(mensagem).strip()) < 20:
            self.errors.append(
                "A mensagem deve possuir pelo menos 20 caracteres."
            )
        elif len(str(mensagem).strip()) > 2000:
            self.errors.append(
                "A mensagem deve ter no máximo 2000 caracteres."
            )

        return len(self.errors) == 0

    def save(self):
        from daos.contato_dao import ContatoDAO
        dao = ContatoDAO()
        return dao.inserir(self)

    def delete(self):
        from daos.contato_dao import ContatoDAO
        dao = ContatoDAO()
        return dao.deletar(self.codigo)

    def update(self):
        from daos.contato_dao import ContatoDAO
        dao = ContatoDAO()
        return dao.atualizar(self.codigo, self)

    @staticmethod
    def contato_by_codigo(codigo):
        from daos.contato_dao import ContatoDAO
        dao = ContatoDAO()
        return dao.buscar_por_codigo(codigo)

    @staticmethod
    def get_all():
        from daos.contato_dao import ContatoDAO
        dao = ContatoDAO()
        return dao.listar_todos()

    @staticmethod
    def get_by_codigo(codigo):
        from daos.contato_dao import ContatoDAO
        dao = ContatoDAO()
        return dao.buscar_por_codigo(codigo)

    @staticmethod
    def get_by_id(id):
        from daos.contato_dao import ContatoDAO
        dao = ContatoDAO()
        return dao.buscar_por_id(id)

    @property
    def codigo(self):
        return self.data.get("codigo")

    @property
    def id(self):
        return self.data.get("id")

    @property
    def data_envio(self):
        return self.data.get("data_envio")

    @property
    def nome(self):
        return self.data.get("nome")

    @property
    def email(self):
        return self.data.get("email")

    @property
    def telefone(self):
        return self.data.get("telefone")

    @property
    def assunto(self):
        return self.data.get("assunto")

    @property
    def mensagem(self):
        return self.data.get("mensagem")
