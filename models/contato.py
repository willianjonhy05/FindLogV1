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

        if not self.data.get("data_envio"):
            self.data["data_envio"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        

        if not self.data.get("codigo"):
            while True:
                codigo = gerar_codigo()

                if not Contato.contato_by_codigo(codigo):
                    self.data["codigo"] = codigo
                    break

                
        def contato_by_codigo(codigo):
            pass


        # self.nome = nome
        # self.email = email
        # self.telefone = telefone
        # self.assunto = assunto
        # self.mensagem = mensagem

    def validate(self, is_new=True):
        self.errors = []

        # Nome (Obrigatório)
        nome = self.data.get("nome")
        if not nome or not str(nome).strip():
            self.errors.append("O nome do usuário não pode ser vazio.")

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

        mensagem = self.data.get("mensagem")

        

        if len(mensagem) < 20:
            self.errors.append("Mensagem de tamanho insuficiente")

        return len(self.errors) == 0
    
    
    @property
    def id(self):
        return self._id

    

    @property
    def data_envio(self):
        return self._data_envio

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O nome é obrigatório.")
        if len(valor.strip()) > 100:
            raise ValueError("O nome deve ter no máximo 100 caracteres.")
        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O e-mail é obrigatório.")

        valor = valor.strip()

        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError("Informe um e-mail válido.")

        self._email = valor

    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O telefone é obrigatório.")
        if len(valor.strip()) > 20:
            raise ValueError("O telefone deve ter no máximo 20 caracteres.")
        self._telefone = valor.strip()

    @property
    def assunto(self):
        return self._assunto

    @assunto.setter
    def assunto(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O assunto é obrigatório.")
        if len(valor.strip()) > 150:
            raise ValueError("O assunto deve ter no máximo 150 caracteres.")
        self._assunto = valor.strip()

    @property
    def mensagem(self):
        return self._mensagem

    @mensagem.setter
    def mensagem(self, valor):
        if not valor or not valor.strip():
            raise ValueError("A mensagem é obrigatória.")
        if len(valor.strip()) > 2000:
            raise ValueError("A mensagem deve ter no máximo 2000 caracteres.")
        self._mensagem = valor.strip()