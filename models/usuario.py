from models.instituicao import Instituicao
from models.sala import Sala

class Usuario:
    def __init__(self, nome, username, email, senha, data_cadastro, instituicao: Instituicao, sala: Sala):

        tipos_de_usuario = {
            1: "Administrador",
            2: "Usuário Comum",
            3: "Servidor"
        }


        self.nome = nome
        self.username = username
        self.foto_perfil = None 
        self.data_nascimento = None 
        self.email = email
        self.senha = senha
        self.data_cadastro = data_cadastro
        self.instituicao = instituicao
        self.sala = sala
        self.ativo = True
        self.tipo_usuario = 1