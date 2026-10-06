from models.categoria import Categoria
from models.instituicao import Instituicao
from models.sala import Sala


class Item:
    def __init__(self, cor, tamanho, data_cadastro, data_devolucao, foto,
                 categoria: Categoria, onde_encontrado, instituicao: Instituicao,
                 quem_encontrou, onde_guardado: Sala):

        self.cor = cor
        self.tamanho = tamanho
        self.data_cadastro = data_cadastro
        self.data_devolucao = data_devolucao
        self.foto = foto
        self.categoria = categoria
        self.onde_encontrado = onde_encontrado
        self.instituicao = instituicao
        self.quem_encontrou = quem_encontrou
        self.onde_guardado = onde_guardado