from models.instituicao import Instituicao
from utils.formata import formatar

class Sala:
    def __init__(self, telefone, andar, numero, instituicao: Instituicao, descricao, predio, laboratorio=False, sala_de_aula=False, codigo=None):
        self.telefone = telefone
        self.andar = andar
        self.numero = numero
        self.instituicao = instituicao
        self.descricao = descricao
        self.predio = predio
        
        # O código é gerado uma única vez na criação e fica fixo (imutável)
        primeira_letra_predio = self.predio.strip()[0].upper()
        self._codigo = f"{primeira_letra_predio}{self.numero}{self.andar}"
        
        self.laboratorio = laboratorio
        self.sala_de_aula = sala_de_aula

    def __str__(self):
        return f"Sala {self.numero} - Andar {self.andar} - Instituição: {self.instituicao.nome}"
    
    @staticmethod
    def get_all():
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        return dao.get_salas()
    
    def save(self):
        from daos.sala_dao import SalaDAO
        dao = SalaDAO()
        resultado = dao.add_sala(self)
        return resultado
    
    @property
    def codigo(self):
        return self._codigo
    
    @property
    def telefone(self):
        return self._telefone
    
    @property
    def andar(self):
        return self._andar
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def instituicao(self):
        return self._instituicao
        
    @property
    def predio(self):
        return self._predio

    @property
    def laboratorio(self):
        return self._laboratorio
    
    @property
    def sala_de_aula(self):
        return self._sala_de_aula
    
    @property
    def descricao(self):
        return self._descricao

    @telefone.setter
    def telefone(self, value):
        if not value:
            raise ValueError("O telefone não pode ser vazio.")
        value = formatar(value)

        if len(value) < 10:
            raise ValueError("O telefone deve possuir pelo menos 10 dígitos.")
        self._telefone = value

    @andar.setter
    def andar(self, value):
        if not value or not str(value).strip():
            raise ValueError("O andar da sala não pode ser vazio.")
        self._andar = str(value).strip()

    @numero.setter
    def numero(self, value):
        if not value or not str(value).strip():
            raise ValueError("O número da sala não pode ser vazio.")
        self._numero = str(value).strip()

    @instituicao.setter
    def instituicao(self, value):
        if not isinstance(value, Instituicao):
            raise ValueError("A instituição da sala precisa ser cadastrada como instituição.")
        self._instituicao = value
        
    @predio.setter
    def predio(self, value):
        if not value or not value.strip():
            raise ValueError("O prédio da sala não pode ser vazio.")
        self._predio = value.strip()

    @laboratorio.setter
    def laboratorio(self, value):
        if not isinstance(value, bool):
            raise ValueError("O campo 'laboratorio' deve ser um valor booleano.")
        self._laboratorio = value

    @sala_de_aula.setter
    def sala_de_aula(self, value):
        if not isinstance(value, bool):
            raise ValueError("O campo 'sala_de_aula' deve ser um valor booleano.")
        self._sala_de_aula = value
        
    @descricao.setter
    def descricao(self, value):
        if not value or not value.strip():
            raise ValueError("A descrição da sala não pode ser vazia.")
        self._descricao = value.strip()