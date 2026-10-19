from datetime import datetime
import unicodedata
import re
from werkzeug.security import generate_password_hash, check_password_hash
from models.instituicao import Instituicao
from models.sala import Sala
from utils.email import validar_email
from utils.formata import formatar

class Usuario:
    TIPOS_USUARIO = {
        1: "Administrador",
        2: "Usuário Comum",
        3: "Servidor"
    }

    def __init__(self, data=None):
        self.data = data or {}
        self.errors = []

        # Valores padrão
        if "ativo" not in self.data:
            self.data["ativo"] = True
        
        if "tipo_usuario" not in self.data:
            self.data["tipo_usuario"] = 1  # Padrão: Administrador

        # Data de cadastro preenchida automaticamente se não existir
        if not self.data.get("data_cadastro"):
            self.data["data_cadastro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Username único e imutável gerado automaticamente se não existir
        nome = self.data.get("nome")
        if nome and not self.data.get("username"):
            self.data["username"] = self._gerar_username_unico(nome)

    def __str__(self):
        return self.data.get("nome", "Usuário sem nome")

    def validate(self, is_new=True):
        self.errors = []

        # Nome (Obrigatório)
        nome = self.data.get("nome")
        if not nome or not str(nome).strip():
            self.errors.append("O nome do usuário não pode ser vazio.")

        # CPF (Obrigatório e único)
        cpf = self.data.get("cpf")
        if not cpf or not str(cpf).strip():
            self.errors.append("O CPF não pode ser vazio.")
        else:
            cpf_limpo = formatar(str(cpf))
            if len(cpf_limpo) != 11:
                self.errors.append("O CPF deve conter exatamente 11 dígitos.")
            elif is_new and Usuario.get_by_cpf(cpf_limpo):
                self.errors.append("Já existe um usuário cadastrado com este CPF.")

        # Data de Nascimento (Obrigatório)
        if not self.data.get("data_nascimento"):
            self.errors.append("A data de nascimento é obrigatória.")

        # E-mail (Obrigatório e válido)
        email = self.data.get("email")
        if not email or not str(email).strip():
            self.errors.append("O e-mail não pode ser vazio.")
        else:
            email_valido = validar_email(email)
            if isinstance(email_valido, str):
                self.errors.append(email_valido)

        # Senha (Obrigatório na criação)
        if is_new and not self.data.get("senha"):
            self.errors.append("A senha é obrigatória.")

        # Instituição (Obrigatório e deve existir)
        instituicao_cnpj = self.data.get("instituicao")
        if not instituicao_cnpj:
            self.errors.append("A instituição é obrigatória.")
        else:
            inst = Instituicao.get_by_cnpj(instituicao_cnpj)
            if not inst:
                self.errors.append("A instituição selecionada não existe.")

        # Regra da Sala: Obrigatório apenas se tipo_usuario for 3 (Servidor)
        tipo_usuario = self.data.get("tipo_usuario")
        sala_codigo = self.data.get("sala")
        if tipo_usuario == 3 and not sala_codigo:
            self.errors.append("O campo de sala é obrigatório para usuários do tipo Servidor.")
        elif sala_codigo:
            sala = Sala.get_by_codigo(sala_codigo)
            if not sala:
                self.errors.append("A sala selecionada não existe.")

        # Telefone (Opcional, mas validado se preenchido)
        telefone = self.data.get("telefone")
        if telefone and str(telefone).strip():
            tel_limpo = formatar(str(telefone))
            if len(tel_limpo) < 10:
                self.errors.append("O telefone deve possuir pelo menos 10 dígitos.")

        return len(self.errors) == 0

    @staticmethod
    def _gerar_base_username(nome):
        """Transforma o nome em um slug base para o username (ex: 'Maria Silva' -> 'maria.silva')"""
        if not nome:
            return "usuario"
        nfkd_form = unicodedata.normalize('NFKD', nome)
        texto_sem_acento = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        username = texto_sem_acento.lower()
        username = re.sub(r'[^a-z0-9\s]', '', username)
        username = re.sub(r'\s+', '.', username).strip('.')
        return username or "usuario"

    @classmethod
    def _gerar_username_unico(cls, nome):
        """Garante que o username gerado seja único no banco de dados"""
        base = cls._gerar_base_username(nome)
        username = base
        contador = 1
        
        while cls.get_by_username(username):
            username = f"{base}.{contador}"
            contador += 1
            
        return username

    def save(self):
        # Criptografa a senha antes de salvar
        if self.data.get("senha") and not self.data["senha"].startswith("pbkdf2:"):
            self.data["senha"] = generate_password_hash(self.data["senha"])
        
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.add_usuario(self)

    def update(self):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.atualizar_usuario(self)


    def atualizar_perfil(self, dados):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.atualizar_dados_perfil(self.username, dados)

    def delete(self):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.deletar_usuario(self.username)


    def alterar_senha(self, senha_atual, nova_senha):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.atualizar_senha(self.username, senha_atual, nova_senha)

    def verificar_senha(self, senha_digitada):
        """Compara a senha em texto plano com o hash armazenado no banco."""
        senha_hash = self.data.get("senha")
        if not senha_hash:
            return False
        return check_password_hash(senha_hash, senha_digitada)    

    @staticmethod
    def get_all():
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.get_usuarios()

    @staticmethod
    def get_all_by_instituicao(cnpj):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.get_usuarios_by_instituicao(cnpj)    

    @staticmethod
    def get_by_username(username):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.get_usuario_by_username(username)

    @staticmethod
    def buscar_nome_por_username(username):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.get_nome_usuario_by_username(username)

    @staticmethod
    def get_by_email(email):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.get_usuario_by_email(email)

    @staticmethod
    def get_by_cpf(cpf):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.get_usuario_by_cpf(formatar(str(cpf)))

    # ==========================
    # PROPRIEDADES (Getters e Setters)
    # ==========================

    @property
    def nome(self):
        return self.data.get("nome")

    @property
    def primeiro_nome(self):
        nome_completo = self.data.get("nome")
        if not nome_completo:
            return "Usuário"
        lista_nome = nome_completo.split()
        return lista_nome[0] if lista_nome else "Usuário"

    @property
    def idade(self):
        from datetime import date
        
        # Pega a string de data de nascimento do dicionário
        data_nasc_str = self.data.get("data_nascimento")
        if not data_nasc_str:
            return None  # Retorna None caso não esteja preenchida
            
        # Converte a string "AAAA-MM-DD" para um objeto date do Python
        # Se ela já for um objeto date/datetime, o fromisoformat lida bem ou podemos checar o tipo
        if isinstance(data_nasc_str, str):
            ano, mes, dia = map(int, data_nasc_str.split("-"))
            nascimento = date(ano, mes, dia)
        else:
            nascimento = data_nasc_str  # Caso já seja um objeto de data

        hoje = date.today()
        
        # Calcula a idade considerando se já fez aniversário este ano
        idade = (
            hoje.year
            - nascimento.year
            - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        )
        
        return idade


    @nome.setter
    def nome(self, value):
        if not value or not str(value).strip():
            raise ValueError("O nome não pode ser vazio.")
        self.data["nome"] = value.strip()

    @property
    def username(self):
        return self.data.get("username")  # Imutável (sem setter)

    @property
    def email(self):
        return self.data.get("email")

    @email.setter
    def email(self, value):
        valido = validar_email(value)
        if isinstance(valido, str):
            raise ValueError(valido)
        self.data["email"] = value.strip()

    @property
    def senha(self):
        return self.data.get("senha")

    @senha.setter
    def senha(self, value):
        if not value or not str(value).strip():
            raise ValueError("A senha não pode ser vazia.")
        # Criptografa imediatamente ao alterar a senha
        self.data["senha"] = generate_password_hash(value)

    @property
    def cpf(self):
        return self.data.get("cpf")

    @cpf.setter
    def cpf(self, value):
        limpo = formatar(str(value))
        if len(limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos.")
        self.data["cpf"] = limpo

    @property
    def data_nascimento(self):
        return self.data.get("data_nascimento")

    @data_nascimento.setter
    def data_nascimento(self, value):
        if not value:
            raise ValueError("A data de nascimento é obrigatória.")
        self.data["data_nascimento"] = value

    @property
    def data_cadastro(self):
        return self.data.get("data_cadastro")  # Automático (sem setter)


    @property
    def instituicao(self):
        return self.data.get("instituicao")

    @property
    def nome_instituicao(self):
        from models.instituicao import Instituicao
        cnpj = self.data.get("instituicao")
        nome = Instituicao.nome_por_cnpj(cnpj)
        if nome:
            return nome
        else:
            return "Inválido"

    @instituicao.setter
    def instituicao(self, value):
        if not value:
            raise ValueError("A instituição é obrigatória.")
        self.data["instituicao"] = value

    @property
    def sala(self):
        return self.data.get("sala")

    @sala.setter
    def sala(self, value):
        self.data["sala"] = value  # Opcional (exceto se Servidor, validado no validate)

    @property
    def foto_perfil(self):
        return self.data.get("foto_perfil")

    @foto_perfil.setter
    def foto_perfil(self, value):
        self.data["foto_perfil"] = value  # Salva o nome/caminho do arquivo de imagem

    @property
    def tipo_usuario(self):
        return self.data.get("tipo_usuario", 1)

    @tipo_usuario.setter
    def tipo_usuario(self, value):
        if value not in self.TIPOS_USUARIO:
            raise ValueError("Tipo de usuário inválido.")
        self.data["tipo_usuario"] = int(value)

    @property
    def ativo(self):
        return self.data.get("ativo", True)

    @ativo.setter
    def ativo(self, value):
        if not isinstance(value, bool):
            raise ValueError("O status ativo deve ser booleano.")
        self.data["ativo"] = value

    @property
    def telefone(self):
        return self.data.get("telefone")

    @telefone.setter
    def telefone(self, value):
        if value and str(value).strip():
            limpo = formatar(str(value))
            if len(limpo) < 10:
                raise ValueError("O telefone deve possuir pelo menos 10 dígitos.")
            self.data["telefone"] = limpo
        else:
            self.data["telefone"] = None


    @staticmethod
    def contar_total():
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.contar_total()


    @staticmethod
    def quantidade_de_usuarios_por_instituicao(cnpj):
        from daos.usuario_dao import UsuarioDAO
        dao = UsuarioDAO()
        return dao.qtd_usuarios_na_instituicao(cnpj)
