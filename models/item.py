from models.categoria import Categoria


class Item:
    def __init__(self, cor, tamanho, data, foto,
                 categoria: Categoria, onde_encontrado,
                 quem_encontrou, onde_guardado):

        self.cor = cor
        self.tamanho = tamanho
        self.data = data
        self.foto = foto
        self.categoria = categoria
        self.onde_encontrado = onde_encontrado
        self.quem_encontrou = quem_encontrou
        self.onde_guardado = onde_guardado