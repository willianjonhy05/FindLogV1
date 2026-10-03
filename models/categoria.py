class Categoria:
    def __init__(self, nome, codigo, descricao):
        self.nome = nome
        self.codigo = codigo
        self.descricao = descricao

    def __str__(self):
        return self.nome

    def save(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.add_categoria(self)

    @staticmethod
    def get_all():
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.get_categorias()

    @staticmethod
    def get_by_codigo(codigo):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        return dao.get_categoria_by_codigo(codigo)

    def delete(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        dao.deletar_categoria(self.codigo)

    def update(self):
        from daos.categoria_dao import CategoriaDAO
        dao = CategoriaDAO()
        dao.atualizar_categoria(self)

    # ==========================
    # NOME
    # ==========================

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        if not value or not value.strip():
            raise ValueError("O nome da categoria não pode ser vazio.")

        self._nome = value.strip()

    # ==========================
    # CÓDIGO
    # ==========================

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, value):
        if not value:
            raise ValueError("O código da categoria não pode ser vazio.")

        if not isinstance(value, int):
            raise ValueError("O código deve ser um número inteiro.")

        self._codigo = value

    # ==========================
    # DESCRIÇÃO
    # ==========================

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        if not value or not value.strip():
            raise ValueError("A descrição não pode ser vazia.")

        self._descricao = value.strip()