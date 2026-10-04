class Item:
    def __init__(self, cor, tamanho, data, foto, categoria,
                 onde_encontrado, quem_encontrou, onde_guardado):
        self.cor = cor
        self.tamanho = tamanho
        self.data = data
        self.foto = foto
        self.categoria = categoria
        self.onde_encontrado = onde_encontrado
        self.quem_encontrou = quem_encontrou
        self.onde_guardado = onde_guardado

    def __str__(self):
        return str(self.categoria)

    def save(self):
        from daos.item_dao import ItemDAO
        return ItemDAO().add_item(self)

    @staticmethod
    def get_all():
        from daos.item_dao import ItemDAO
        return ItemDAO().get_itens()